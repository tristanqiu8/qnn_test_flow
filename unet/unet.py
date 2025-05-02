import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.LeakyReLU(0.2, inplace=True)
        )
    
    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 编码器（通道数规则：输入11→输出16，中间层保持16）
        self.inc = ConvBlock(11, 16)          # 输入11→输出16
        self.down1 = nn.MaxPool2d(2)
        self.conv1 = ConvBlock(16, 16)        # 保持16通道
        self.down2 = nn.MaxPool2d(2)
        self.conv2 = ConvBlock(16, 16)        # 保持16通道
        self.down3 = nn.MaxPool2d(2)
        self.conv3 = ConvBlock(16, 16)        # 保持16通道
        
        # 解码器（通道数规则：输入16→输出16，拼接后32→16）
        self.up1 = nn.ConvTranspose2d(16, 16, 2, stride=2)
        self.up_conv1 = ConvBlock(32, 16)     # 拼接后32→16
        self.up2 = nn.ConvTranspose2d(16, 16, 2, stride=2)
        self.up_conv2 = ConvBlock(32, 16)     # 拼接后32→16
        self.up3 = nn.ConvTranspose2d(16, 16, 2, stride=2)
        self.up_conv3 = ConvBlock(32, 16)     # 拼接后32→16
        
        # 输出层（末层16→3）
        self.outc = nn.Conv2d(16, 3, 1)       # 最终输出3通道

    def forward(self, x):
        # 编码器
        x1 = self.inc(x)       # [1,16,224,224]
        x2 = self.down1(x1)
        x2 = self.conv1(x2)    # [1,16,112,112]
        x3 = self.down2(x2)
        x3 = self.conv2(x3)    # [1,16,56,56]
        x4 = self.down3(x3)
        x4 = self.conv3(x4)    # [1,16,28,28]
        
        # 解码器
        x = self.up1(x4)       # [1,16,56,56]
        x = torch.cat([x, x3], dim=1)  # 通道拼接→[1,32,56,56]
        x = self.up_conv1(x)   # →[1,16,56,56]
        x = self.up2(x)        # →[1,16,112,112]
        x = torch.cat([x, x2], dim=1)
        x = self.up_conv2(x)
        x = self.up3(x)        # →[1,16,224,224]
        x = torch.cat([x, x1], dim=1)
        x = self.up_conv3(x)
        return self.outc(x)    # [1,3,224,224]

# 验证模型
model = UNet()
dummy_input = torch.randn(1, 11, 256, 256)  # Batch固定为1
output = model(dummy_input)
print("输出形状:", output.shape)  # 应为torch.Size([1,3,224,224])

def export_onnx():
    model.eval()
    torch.onnx.export(
        model,
        dummy_input,
        "unet.onnx",
        export_params=True,
        opset_version=16,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes=None  # 固定Batch维度为1
    )
    print("ONNX导出完成")

export_onnx()