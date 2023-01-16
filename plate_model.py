import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
from img_deal import get_img_one, get_img_data


# 车牌识别的类
class plate_model():
    def __init__(self):
        self.hight = 80  # 图片高度
        self.width = 240  # 图片宽度
        self.classes = 68  # 预测类别数
        self.epochs = 100  # 训练次数
        self.model_save_path = './cnn_model.h5'  # 模型保存路径

    # 模型训练
    def train(self):
        # def train(self,imgss,labels):
        # 获取数据
        imgss, labels = get_img_data()
        # 车牌图片shape(80,240,1)
        Input = layers.Input((self.hight, self.width, 1))
        # 卷积
        x = layers.Conv2D(filters=16, kernel_size=(3, 3), strides=1)(Input)
        # 池化
        x = layers.MaxPool2D(pool_size=(2, 2), strides=2)(x)
        # 添加3个类似的卷积池化
        for i in range(3):
            x = layers.Conv2D(filters=32 * 2 ** i, kernel_size=(3, 3))(x)
            x = layers.Conv2D(filters=32 * 2 ** i, kernel_size=(3, 3))(x)
            x = layers.MaxPool2D(pool_size=(2, 2), strides=2)(x)
            # 丢弃层，防止过拟合
            x = layers.Dropout(0.5)(x)
        # 拉直
        x = layers.Flatten()(x)
        # 丢弃层
        x = layers.Dropout(0.3)(x)
        # # 输出层，7个输出，每个输出都是68个字符的概率
        Output = [layers.Dense(self.classes, activation='softmax', name='c%d' % (i + 1))(x) for i in
                  range(7)]  # 7个输出分别对应车牌7个字符，每个输出都为65个类别类概率
        # 输入输出构成模型
        model = models.Model(inputs=Input, outputs=Output)
        # 保存节点，监控损失值，只保存最好的，损失最小的模型
        checkpoint = ModelCheckpoint(self.model_save_path, monitor='loss', verbose=1,
                                     save_best_only=True, mode='min', save_freq=2)
        # 模型编译
        model.compile(optimizer='adam',
                      # 输出未进行one-hot编码，是离散型的数值
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # 模型训练
        print("开始训练cnn...")
        model.fit(imgss, labels, epochs=self.epochs,
                  callbacks=[checkpoint])
        model.save(self.model_save_path)
        print('模型训练保存成功!!!')

    # 模型预测
    def predict(self, filename):
        # 读取单张图片
        imagedata, imgss, labels = get_img_one(file_name=filename)  # 重定向为预测输入方法的图片路径
        # imagedata, imgss, labels = get_img_one()
        # print('请稍候...')
        # 导入模型
        cnn = load_model(self.model_save_path)  # 调用模型预测
        # 预测结果，预测数据的形状应为(1,80,240,1)
        lic_pred = cnn.predict(tf.reshape(imgss, (1, self.hight, self.width, 1)))
        # 将结果更改为7*68的数组
        lic_pred = np.array(lic_pred).reshape(7, self.classes)
        # 输出68个结果对应的最大概率
        pres = list(np.argmax(lic_pred, axis=1))
        province = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑",
                    "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤",
                    "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁",
                    "新", "警", "学", "O"]
        nums = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6',
                '7', '8', '9']
        chars = ''

        for i in range(7):  # 循环7个字符对应的数值,将其转为字符
            if i == 0:  # 第0个字符为省份，对应省份的字符
                chars += province[pres[i]]
            else:  # 第一个字符开始为数值和字母
                chars += nums[pres[i]]
        # 字符中间加上‘.’
        chars = chars[0:2] + '·' + chars[2:]
        # 可视化
        import matplotlib
        # matplotlib.use('TKAgg')
        matplotlib.use('Agg')  # 控制绘图不显示
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.imshow(imagedata)
        plt.title('预测结果：' + chars, c='r')
        # plt.show()
        print("此次模型预测结果为" + chars)
        print(chars)
        return chars


if __name__ == '__main__':
    # 模型实例化
    model = plate_model()
    # 执行模型训练
    # model.train()
    # 执行模型预测
    # model.predict("0079-0_1-262&573_398&622-398&620_264&622_262&575_396&573-0_12_4_24_32_32_10-152-40.jpg")
