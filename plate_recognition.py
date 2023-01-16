# coding=utf-8
from img_deal import img2plate
from plate_model import plate_model


def get_plate_name(file_name):
    # 车牌截取和处理
    # img2plate()

    model = plate_model()  # 模型实例化

    # model.train() # 执行模型训练

    # model.predict() # 执行模型预测
    result = model.predict(file_name)
    return result


if __name__ == '__main__':
    img_name = "0060-3_0-484&480_597&525-597&518_487&525_484&487_594&480-10_2_3_27_25_29_5-64-9.jpg"
    get_plate_name(img_name)
    # 测试车牌识别
