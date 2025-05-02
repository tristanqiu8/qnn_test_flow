import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = self.shortcut(x)
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity
        return torch.relu(out)

class ResNet18(nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super().__init__()
        self.in_channels = 64
        
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 64, 7, 2, 3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, 2, 1)
        )
        
        self.layers = nn.Sequential(
            self._make_layer(64, 64, 2, stride=1),   # layer1
            self._make_layer(64, 128, 2, stride=2), # layer2
            self._make_layer(128, 256, 2, stride=2), # layer3
            self._make_layer(256, 512, 2, stride=2)  # layer4
        )
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)
    
    def _make_layer(self, in_dim, out_dim, blocks, stride):
        layers = [ResidualBlock(in_dim, out_dim, stride)]
        for _ in range(1, blocks):
            layers.append(ResidualBlock(out_dim, out_dim))
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.layers(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return self.fc(x)
    
def export_onnx():
    # 参数配置
    BATCH_SIZE = 1
    IN_CHANNELS = 3
    IMG_SIZE = 224
    NUM_CLASSES = 1000
    
    # 初始化模型
    model = ResNet18(in_channels=IN_CHANNELS, num_classes=NUM_CLASSES)
    model.eval()
    
    # 构造虚拟输入（固定形状）
    dummy_input = torch.randn(
        BATCH_SIZE, 
        IN_CHANNELS, 
        IMG_SIZE, 
        IMG_SIZE
    )
    
    # 导出ONNX
    torch.onnx.export(
        model,
        dummy_input,
        "resnet18_titan.onnx",
        export_params=True,
        opset_version=16,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes=None  # 禁用动态轴
    )

if __name__ == "__main__":
    export_onnx()