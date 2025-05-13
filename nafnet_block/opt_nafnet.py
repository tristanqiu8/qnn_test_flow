import onnx
from onnxoptimizer import optimize

model = onnx.load("./nafnet_block/nafnet_block_dyt.onnx")

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
    if node.op_type == 'Conv' and model.graph.node[idx+1].op_type == 'Mul':
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
    passes=['fuse_consecutive_transposes']
)
onnx.checker.check_model(optimized_model)
onnx.save(optimized_model, "./nafnet_block/naf_block_opt.onnx")