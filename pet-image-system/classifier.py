# classifier.py —— 图片识别模块（模型在程序启动时加载一次）
import torch
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
from PIL import Image

_weights = MobileNet_V3_Small_Weights.DEFAULT
_model = mobilenet_v3_small(weights=_weights)
_model.eval()
_categories = _weights.meta["categories"]
_transform = _weights.transforms()


def classify(image_path: str) -> tuple[str, float]:
    """输入图片路径，返回 (类别名, 置信度)"""
    image = Image.open(image_path).convert("RGB")
    tensor = _transform(image).unsqueeze(0)
    with torch.no_grad():
        scores = _model(tensor)
    prob = torch.nn.functional.softmax(scores, dim=1)
    confidence, index = torch.max(prob, 1)
    return _categories[index.item()], round(confidence.item(), 4)