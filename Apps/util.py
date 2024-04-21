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