import onnx
from onnxoptimizer import optimize
from onnx import shape_inference
import numpy as np

model = onnx.load("./nafnet_block/nafnet_block_dyt.onnx")
model = shape_inference.infer_shapes(model)

for idx, node in enumerate(model.graph.node):  # four dytanh into one
    # 假设ABC连续排列且名称包含特征（如残差块标识）
    if node.op_type == 'Mul' and model.graph.node[idx+1].op_type == 'Tanh' \
       and model.graph.node[idx+2].op_type == 'Mul' and model.graph.node[idx+3].op_type == 'Add':
        node_a = node
        node_b = model.graph.node[idx+1]
        node_c = model.graph.node[idx+2]
        node_d = model.graph.node[idx+3]

        # 将原A的输入赋予B
        node_b.input[0] = node_a.input[1]
        # 将B的输出指向原D的后续节点
        if idx + 4 < len(model.graph.node):
            next_node = model.graph.node[idx+4]
            next_node.input[0] = node_b.output[0]
        else:
            print(f"Warning: Node at index {idx+4} does not exist. Skipping connection.")
        # 这里可以添加对节点的处理逻辑
        model.graph.node.remove(node_a)
        model.graph.node.remove(node_c)
        model.graph.node.remove(node_d)

for idx, node in enumerate(model.graph.node):  # fuse conv and mul
    if node.op_type == 'Conv' and model.graph.node[idx+1].op_type == 'Mul' and node.name != 'Conv_19':
        node_a = node
        node_b = model.graph.node[idx+1]

        # detete node_b
        # 将B的输出指向原D的后续节点
        if idx + 2 < len(model.graph.node):
            next_node = model.graph.node[idx+2]
            for i, input_name in enumerate(next_node.input):
                if input_name == node_b.output[0]:
                    index = i
                    break
            next_node.input[index] = node_a.output[0]
        else:
            print(f"Warning: Node at index {idx+2} does not exist. Skipping connection.")
        # 这里可以添加对节点的处理逻辑
        model.graph.node.remove(node_b)

optimized_model = optimize(
    model,
    passes=['fuse_consecutive_transposes', 'eliminate_deadend', 'fuse_consecutive_concats']
)
onnx.checker.check_model(optimized_model)
onnx.save(optimized_model, "./nafnet_block/naf_no_add_convert.onnx")

for idx, node in enumerate(model.graph.node):  # Convert elementwise add into Concat + Conv
    if node.op_type == 'Add':
        from onnx import helper, numpy_helper

        # 生成新节点名称
        concat_output = f"{node.name}_concat"
        conv_output = node.output[0]

        # 创建Concat节点 (axis=1为通道维度)
        concat_node = helper.make_node(
            'Concat', 
            inputs=node.input,  # 原Add的输入A/B
            outputs=[concat_output],
            name=f"{node.name}_concat",
            axis=1
        )

        # 创建Conv权重 (C=输入通道数, 2C为合并后的输入通道)
        # Search in both graph inputs and value info for shape information
        input_shape = None
        for vi in list(model.graph.input) + list(model.graph.value_info):
            if vi.name == node.input[0]:
                input_shape = vi.type.tensor_type.shape.dim
                break
        if input_shape is None:
            raise ValueError(f"Could not find shape information for {node.input[0]}")
        C = input_shape[1].dim_value  # 假设静态通道维度
        weights = numpy_helper.from_array(
            np.ones((C, 2, 1, 1), dtype=np.float32), 
            name=f"{node.name}_conv_weight"
        )

        # 创建Conv节点
        conv_node = helper.make_node(
            'Conv',
            inputs=[concat_output, weights.name],
            outputs=[conv_output],
            name=f"{node.name}_conv",
            kernel_shape=[1, 1],
            strides=[1, 1],
            pads=[0, 0, 0, 0],
            group=C
        )

        # 删除原Add节点
        model.graph.node.remove(node)

        # 插入新节点到原Add位置

        model.graph.node.insert(idx, concat_node)
        model.graph.node.insert(idx+1, conv_node)

        # 添加权重到initializer
        model.graph.initializer.append(weights)
        
# for idx, node in enumerate(model.graph.node):  # fuse two conv into one
#     if node.name == 'Conv_19' and model.graph.node[idx+1].name == 'Conv_21':
#         node_a = node
#         node_b = model.graph.node[idx+1]

#         # detete node_b
#         # 将B的输出指向原D的后续节点
#         if idx + 2 < len(model.graph.node):
#             next_node = model.graph.node[idx+2]
#             for i, input_name in enumerate(next_node.input):
#                 if input_name == node_b.output[0]:
#                     index = i
#                     break
#             next_node.input[index] = node_a.output[0]
#         else:
#             print(f"Warning: Node at index {idx+2} does not exist. Skipping connection.")
#         # 这里可以添加对节点的处理逻辑
#         model.graph.node.remove(node_b)

optimized_model = optimize(
    model,
    passes=['fuse_consecutive_transposes', 'eliminate_deadend', 'fuse_consecutive_concats']
)
onnx.checker.check_model(optimized_model)
onnx.save(optimized_model, "./nafnet_block/naf_block_opt.onnx")