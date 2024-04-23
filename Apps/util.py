# 导入必要的库
import os
import joblib
import numpy as np
import cv2 as cv
from skimage import io


# 定义预处理图像函数
def preprocess_image(file_name, new_size):
    # 1. 读取图像灰度图
    img = io.imread(file_name, as_gray=True)
    # 归一化
    img = img / 255
    # 2. 调整图像大小为 new_size
    img = cv.resize(img, new_size, interpolation=cv.INTER_CUBIC)
    # 3. 将图像展平为一维数组
    return img.ravel()


# 定义预测函数
def predict_font(image_path):
    # 加载模型
    model_path = "./Apps/best_model"  # 指定模型路径./best_model
    model = joblib.load(model_path)

    # 预处理图像
    img = preprocess_image(image_path, new_size=[100, 100])  # 指定图像大小

    # 使用加载的模型进行预测
    predicted_class = model.predict([img])[0]

    # 获取预测结果对应的字体样式
    char_styles = ["篆书", "隶书", "草书", "行书", "楷书"]
    predicted_font = char_styles[int(predicted_class)]

    # 打印预测结果
    print("预测类别:", predicted_font)
    return predicted_font

# # 测试预测函数
# image_file_path = "./Apps/test.jpg"  # 图片文件路径
# predict_font(image_file_path)

#-----书法字

import torch
from torchvision import transforms
from PIL import Image
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 25 * 25, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# 定义类别标签列表
classes = ['上', '与', '信', '大', '学', '工', '师', '年', '息', '机', '测', '海', '电', '程', '范', '院']

# 创建映射字典
index_to_label = {i: label for i, label in enumerate(classes)}

# 图像转换
transform = transforms.Compose([
    transforms.Resize((200, 200)),
    transforms.Grayscale(num_output_channels=3),  # 将图像转换为三通道的灰度图像
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def predict_calligraphy(image_path):
    model_path = './Apps/calligraphy_model.pth'
    # 创建模型实例
    model = CNN(num_classes=len(classes))

    # 加载模型权重
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 加载要验证的图像
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # 添加一个维度作为批次维度

    # 使用模型进行预测
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        predicted_label = classes[predicted.item()]

    return predicted_label
