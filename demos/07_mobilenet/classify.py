import torch
from torchvision.models import mobilenet_v3_small,MobileNet_V3_Small_Weights
from PIL import Image

#1.加载预训练模型
weights=MobileNet_V3_Small_Weights.DEFAULT
model=mobilenet_v3_small(weights=weights)
model.eval()
categories=weights.meta["categories"]

#2.预处理（weights自带标准做法 ：缩放 裁剪 转张量 归一化）
transform=weights.transforms()


#3.读图片
image=Image.open("test01.jpg").convert("RGB")
tensor=transform(image).unsqueeze(0)

#4.推理
with torch.no_grad():
    scores=model(tensor)
    
#5.取概率最高的类别
prob=torch.nn.functional.softmax(scores,dim=1)
confidence,index=torch.max(prob,1)
print("类别：",categories[index.item()],"| 置信度：",round(confidence.item(),4))