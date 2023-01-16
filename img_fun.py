import cv2
import numpy as np
from PIL import Image

import matplotlib.pyplot as pyplot


# 图像功能py文件

# 直方图均衡化：图像增强
def equ_hist(img):
    img2 = img.copy()  # 简单地返回图像的副本
    # R、G、B三个通道都进行增强
    for i in [0, 1, 2]:
        img2[:, :, i] = cv2.equalizeHist(img[:, :, i])
        # EqualizeHist函数直方图均衡化，用于提高图像的质量
    return img2


# 霍夫变换:图片倾斜矫正
def Hough_rotation(gray):
    import math
    from scipy import misc, ndimage
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # 将输入的原始图像转换为边缘图像
    # 霍夫变换
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)  # 使用Hough检测直线
    rho, theta = lines[0][0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    t = float(y2 - y1) / (x2 - x1) if x2 != x1 else 0
    rotate_angle = math.degrees(math.atan(t))  # 将弧度转换为角度
    if rotate_angle > 45:
        rotate_angle = -90 + rotate_angle
    elif rotate_angle < -45:
        rotate_angle = 90 + rotate_angle
    image = Image.fromarray(gray)  # 实现array到image的转换
    rotate_img = image.rotate(rotate_angle)  # 用于将给定图像围绕其中心逆时针旋转到给定度数
    return np.array(rotate_img)


# 分段线性变换函数来增强图像对比度
def SLT(img, x1, x2, y1, y2):
    # 分段线性变换函数来增强图像对比度的方法实际是增强原图各部分的反差，
    # 即增强输入图像中感兴趣的灰度区域，相对抑制那些不感兴趣的灰度区域。
    # 增分段线性函数的主要优势在于它的形式可任意合成，而其缺点是需要更多的用户输入。
    lut = np.zeros(256)  # 返回来一个给定形状和类型的用0填充的数组
    for i in range(256):
        if i < x1:
            lut[i] = (y1 / x1) * i
        elif i < x2:
            lut[i] = ((y2 - y1) / (x2 - x1)) * (i - x1) + y1
        else:
            lut[i] = ((y2 - 255.0) / (x2 - 255.0)) * (i - 255.0) + 255.0
    img_output = cv2.LUT(img, lut)  # 用于灰度图像转换为彩色图像，自定义色谱映射表 lut
    img_output = np.uint8(img_output + 0.5)  # 对原数据和0xff相与(和最低2字节数据相与)
    return img_output


# 图像二值化和矫正
def Rotation(gray):
    t = int(np.tanh(np.mean(gray) - 120) * 20 + 100)
    e = 200 if t < 200 else t + 1
    # 分段线性变换
    img_correct = SLT(gray, t, e, 20, 240)
    # 图像二值化
    ret, bi_image = cv2.threshold(img_correct, 170, 255, cv2.THRESH_OTSU)  # 对单通道数组应用固定阈值操作
    # 霍夫变换:图片倾斜矫正
    rotate_img = Hough_rotation(bi_image)
    return rotate_img


def cut_lines(gray):  # 这里可以对二维数组图像进行边框剔除【没必要】

    # print(list(np.array(gray).flatten()))  # 输出二维转一维
    # gray1 = list(np.array(gray).flatten())
    # image = Image.fromarray(gray)  # 实现array到image的转换
    # image.save("out.jpg")  # 实时输出查看

    return gray
