import cv2
import os
import numpy as np
import tensorflow as tf

from img_fun import equ_hist, Rotation, cut_lines


# 图像处理py文件


# 对文件夹下的文件处理
def img2plate(image_path='./data',
              plate_save_path='./plate',
              plate_process_path='./plate_after_process'):
    '''
    :param image_path: 汽车图像数据
    :param plate_save_path 车牌图像保存路径
    :return:
    '''
    from PlateDetect import PD
    # 类的实例化
    PD = PD()
    # 若文件存在则删除，否则新建
    if not os.path.exists(plate_process_path):
        os.makedirs(plate_process_path)
    print('车牌截取中...')
    # 罗列路径下的所有文件
    file_names = os.listdir(image_path)
    # 批处理：车牌检测
    for file_name in file_names:
        print(f'正在处理{file_names.index(file_name) + 1}/{len(file_names)}')
        # 读取图片
        image = cv2.imread(os.path.join(image_path, file_name))
        # 获取图片结果和物体框的坐标
        _, box = PD.show_inference(os.path.join(image_path, file_name))
        # 找到框出来的位置比例
        ymin, xmin, ymax, xmax = box
        # 图片大小
        image_height, image_width, _ = image.shape
        # 找到车牌坐标点
        left, right, top, bottom = xmin * image_width, xmax * image_width, ymin * image_height, ymax * image_height
        # 车牌截取，稍微放宽位置
        plate_image = image[int(top) - 5: int(bottom) + 5, int(left) - 5:int(right) + 5, :]
        # 车牌保存
        cv2.imwrite(os.path.join(plate_save_path, file_name), plate_image)
        # 直方图均衡化（图像增强）
        image_equ = equ_hist(plate_image)
        # 灰度处理
        gray = cv2.cvtColor(image_equ, cv2.COLOR_BGR2GRAY)
        # 图片倾斜纠正
        image_rot = Rotation(gray)
        # 边框剔除
        image_cut = cut_lines(image_rot)
        # 处理好的车牌保存
        cv2.imwrite(os.path.join(plate_process_path, file_name), image_cut)
    print('车牌图片预处理完成！')


# 获取文件夹下所有文件的数据和标签
def get_img_data(plate_process_path='./plate_after_process'):
    # 列出所以图片
    file_names = os.listdir(plate_process_path)
    imgs = []  # 所有图片汇总
    labels = []  # 所有标签汇总
    # 循环每个图片获取array和label
    for f in file_names:
        # 读取图片
        # 读取图片(灰度图),并取其中一个通道的值，但请注意要保持其维度(三维)不变
        img = cv2.imread(os.path.join(plate_process_path, f))[:, :, 0:1]
        # 更改大小
        img = cv2.resize(img, (80, 240))
        # 增加一维数据
        imgs.append(img.reshape([80, 240, 1]))  # 图片数据
        # 取标签
        labels.append([int(i) for i in list(map(int, f.split('-')[4].split('_')))])  # 标签数据
    # 标准化0-1区间
    imgs = np.array(imgs) / 255
    # 转为tensor
    imgs = tf.convert_to_tensor(imgs)
    # 构造7个元素的列表，每个元素都是68个字符的集合
    labels = [np.array(labels)[:, i] for i in range(7)]
    return imgs, labels


# 获取单张图片的数据和标签
def get_img_one(file_path='./data/'
                , file_name='0060-3_0-484&480_597&525-597&518_487&525_484&487_594&480-0_0_0_0_0_0_0-64-9.jpg'):
    from PlateDetect import PD
    # 类的实例化
    PD = PD()
    # 文件路径拼接
    file = os.path.join(file_path, file_name)
    # 图片读取
    imagedata = cv2.imread(file)
    # 获取图片结果和物体框的坐标
    _, box = PD.show_inference(file)
    # 找到框出来的位置比例
    ymin, xmin, ymax, xmax = box
    # 获取图片的大小
    image_height, image_width, _ = imagedata.shape
    # 找到方框的坐标
    left, right, top, bottom = xmin * image_width, xmax * image_width, ymin * image_height, ymax * image_height
    # 车牌截取，稍微放宽位置
    plate_image = imagedata[int(top) - 5: int(bottom) + 5, int(left) - 5:int(right) + 5, :]
    # 直方图均衡化（图像增强）
    image_equ = equ_hist(plate_image)
    # 灰度处理
    gray = cv2.cvtColor(image_equ, cv2.COLOR_BGR2GRAY)
    # 图片倾斜纠正
    image_rot = Rotation(gray)
    # 边框剔除
    image_cut = cut_lines(image_rot)
    # 更改大小
    img = cv2.resize(image_cut, (80, 240))
    # 增加一维数据
    imgs = img.reshape([80, 240, 1])
    # 转为tensor
    imgss = tf.convert_to_tensor(imgs)
    # 取标签
    labels = [int(i) for i in list(map(int, file_name.split('-')[4].split('_')))]  # 标签数据
    # print('图片处理完成!')
    return imagedata, imgss, labels
