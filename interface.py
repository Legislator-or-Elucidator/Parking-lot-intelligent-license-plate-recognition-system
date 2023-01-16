import time
import random
import pygame
import pandas as pd
from pandas import DataFrame
import os
import csv
import cv2
import matplotlib.pyplot as plt

from operator import itemgetter
from interface_config import btn
from interface_config import timeutil
from plate_recognition import get_plate_name
from interface_config import ocrutil

size = 1200, 800  # 窗体大小，左右：1000(+200),上下:484(+316)
FPS = 60  # 设置帧率（屏幕每秒的刷新次数）
# 设置背景颜色
DARKBLUE = (73, 119, 142)  # R、G、B
BG = DARKBLUE
# 定义颜色
BLACK = (0, 0, 0)  # 黑
WHITE = (255, 255, 255)  # 白
GREEN = (0, 255, 0)  # 绿
BLUE = (72, 61, 139)  # 蓝
GRAY = (96, 96, 96)  # 棕
RED = (220, 20, 60)  # 红
YELLOW = (255, 255, 0)  # 黄

# 信息内容
txt1 = ''
txt2 = ''
txt3 = ''
txt4 = ''

Total = 100  # 一共有多少车位
income_switch1 = False  # 月收入统计分析界面开关
income_switch2 = False  # 月收入统计分析界面开关

# 获取文件的路径
cdir = os.getcwd()

# 文件路径
path = cdir + '/interface_config/datafile/'
if not os.path.exists(path):
    os.makedirs(path)  # 根据路径建立文件夹
    # 车牌号、日期、价格、状态
    carnfile = pd.DataFrame(columns=['carnumber', 'date', 'price', 'state'])
    # 生成.xlsx文件
    carnfile.to_excel(path + '停车场车辆表.xlsx', sheet_name='data')
    carnfile.to_excel(path + '停车场信息表.xlsx', sheet_name='data')

# 读取文件内容
pi_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data')
# print(pi_table)
pi_info_table = pd.read_excel(path + '停车场信息表.xlsx', sheet_name='data')

cars = pi_table[['carnumber', 'date', 'state']].values  # 停车场车辆

carn = len(cars)  # 已进入停车场数量
print('总数量：' + str(carn))

pygame.init()  # 初始化
pygame.display.set_caption('停车场智能车牌识别系统')  # 设置窗体名称

ic_launcher = pygame.image.load('interface_config/file/ic_launcher.jpg')  # 加载图片
pygame.display.set_icon(ic_launcher)  # 设置图标

screen = pygame.display.set_mode(size)  # 设置窗体大小
screen.fill(BG)  # 设置背景颜色


# 背景和信息文字
def text0(screen):
    pygame.draw.rect(screen, BG, (650, 2, 1580, 800))  # 底色  (左右,上下,长,高)

    pygame.draw.aaline(screen, GREEN, (662, 80), (1180, 80), 2)  # 绘制横线 (左，上),(右，上)，粗细

    pygame.draw.rect(screen, GREEN, (650, 580, 542, 150), 2)  # 绘制信息矩形框 (左右,上下,长,高),粗细

    pygame.draw.rect(screen, GREEN, (0, 0, 642, 800), 2)  # 绘制图像矩形框 (左右,上下,长,高),粗细

    xtfont = pygame.font.SysFont('SimHei', 23)  # 使用系统字体
    textstart = xtfont.render('信息', True, GREEN)  # 信息文字

    text_rect = textstart.get_rect()  # 获取文字图像位置
    # 设置文字图像中心点
    text_rect.centerx = 680
    text_rect.centery = 600

    screen.blit(textstart, text_rect)  # 绘制内容


# 表头
def text1(screen):
    xtfont = pygame.font.SysFont('SimHei', 25)
    textstart = xtfont.render('停车场智能车牌识别系统', True, YELLOW)
    text_rect = textstart.get_rect()  # 获取文字图像位置
    # 设置文字图像中心点
    text_rect.centerx = 900
    text_rect.centery = 20

    screen.blit(textstart, text_rect)  # 绘制内容


# 车位文字
def text2(screen):
    k = Total - carn  # 剩余车位
    if k < 10:
        sk = '0' + str(k)
    else:
        sk = str(k)
    xtfont = pygame.font.SysFont('SimHei', 20)
    # local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) # 年/月/日 时/分/秒
    local_time = time.strftime('%H:%M:%S', time.localtime())  # 时/分/秒
    # print("当前时间戳：", local_time)
    textstart = xtfont.render('当前时间:' + local_time +
                              '   共有车位：' + str(Total) +
                              '   剩余车位：' + sk, True, WHITE)
    # 添加文字信息

    text_rect = textstart.get_rect()  # 获取文字图像位置
    # 设置文字图像中心点
    text_rect.centerx = 900
    text_rect.centery = 60
    # 绘制内容
    screen.blit(textstart, text_rect)


# 停车场信息表头
def text3(screen):
    xtfont = pygame.font.SysFont('SimHei', 20)
    textstart = xtfont.render('     车牌号             进入时间', True, WHITE)  # 添加文字信息
    text_rect = textstart.get_rect()  # 获取文字图像位置
    # 设置文字图像中心点
    text_rect.centerx = 900
    text_rect.centery = 100

    screen.blit(textstart, text_rect)  # 绘制内容


# 停车场车辆信息
def text4(screen):
    xtfont = pygame.font.SysFont('SimHei', 14)
    cars = pi_table[['carnumber', 'date', 'state']].values  # 获取停车场车辆信息
    if len(cars) > 10:  # 页面绘制最新10辆车信息
        cars = pd.read_excel(path + '停车场车辆表.xlsx', skiprows=len(cars) - 20, sheet_name='data').values
        n = 0
        for car in cars:  # 循环显示车辆信息
            n += 1
            textstart = xtfont.render(str(car[1]) + '                ' + str(car[2]), True, WHITE)  # 显示车号和进入时间
            # print('     ' + str(car[0]) + '    ' + str(car[1])+'     ' + str(car[2]) + '    ' + str(car[3]))

            text_rect = textstart.get_rect()  # 获取文字图像位置
            # 设置文字图像中心点
            text_rect.centerx = 930
            text_rect.centery = 100 + 20 * n

            # 绘制内容
            screen.blit(textstart, text_rect)


# 最长停放的车辆和时间
def text5(screen):
    cars = pi_table[['carnumber', 'date', 'state']].values

    if len(cars) > 0:
        longcar = cars[0][0]
        cartime = cars[0][1]
        # print(cartime)
        cars2 = pd.read_excel(path + '停车场车辆表.xlsx', skiprows=len(cars) - 20, sheet_name='data').values
        n = 0
        xtfont1 = pygame.font.SysFont('SimHei', 14)
        for car in cars2:  # 循环显示车辆信息
            n += 1
            textstart1 = xtfont1.render(str(car[1]) + '                ' + str(car[2]), True, WHITE)  # 显示车号和进入时间
            # print('     ' + str(car[0]) + '    ' + str(car[1]) + '     ' + str(car[2]) + '    ' + str(car[3]))

            text_rect1 = textstart1.get_rect()  # 获取文字图像位置
            # 设置文字图像中心点
            text_rect1.centerx = 930
            text_rect1.centery = 100 + 20 * n

            # 绘制内容
            screen.blit(textstart1, text_rect1)

        xtfont = pygame.font.SysFont('SimHei', 20)

        # 转换当前时间2022-12-25 19：07
        localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        htime = timeutil.DtCalc(cartime, localtime)

        # 添加文字
        textscar = xtfont.render('停车时间最长车辆：' + str(longcar), True, RED)
        texttime = xtfont.render('已停车：' + str(htime) + '小时', True, RED)
        # 获取文字图像位置
        text_rect1 = textscar.get_rect()
        text_rect2 = texttime.get_rect()
        # 设置文字图像中心点
        text_rect1.centerx = 900
        text_rect1.centery = 530
        text_rect2.centerx = 900
        text_rect2.centery = 555
        # 绘制内容
        screen.blit(textscar, text_rect1)
        screen.blit(texttime, text_rect2)


# 在信息框中显示信息
def text6(screen, txt1, txt2, txt3, txt4):
    xtfont = pygame.font.SysFont('SimHei', 21)

    texttxt1 = xtfont.render(txt1, True, GREEN)
    text_rect = texttxt1.get_rect()
    text_rect.centerx = 900
    text_rect.centery = 600 + 25  # 字数间隔
    screen.blit(texttxt1, text_rect)

    texttxt2 = xtfont.render(txt2, True, GREEN)
    text_rect = texttxt2.get_rect()
    text_rect.centerx = 900
    text_rect.centery = 600 + 50
    screen.blit(texttxt2, text_rect)

    texttxt3 = xtfont.render(txt3, True, GREEN)
    text_rect = texttxt3.get_rect()
    text_rect.centerx = 900
    text_rect.centery = 600 + 75
    screen.blit(texttxt3, text_rect)

    texttxt4 = xtfont.render(txt4, True, GREEN)
    text_rect = texttxt4.get_rect()
    text_rect.centerx = 900
    text_rect.centery = 600 + 100
    screen.blit(texttxt4, text_rect)


# 进场出场内容
def text7(screen, welcome_txt):
    pygame.draw.rect(screen, YELLOW, ((2, 2), (640, 60)))
    xtfont = pygame.font.SysFont('SimHei', 20)
    text_welcome = xtfont.render(welcome_txt, True, RED)
    text_rect = text_welcome.get_rect()
    text_rect.centerx = 322
    text_rect.centery = 30
    screen.blit(text_welcome, text_rect)


# 收入统计
def text8(screen):
    # 计算price列的和
    sum_price = pi_info_table['price'].sum()
    # 使用系统字体
    xt1font = pygame.font.SysFont('SimHei', 24)
    xtfont = pygame.font.SysFont('SimHei', 20)
    # 表头
    text_title = xt1font.render('停车场日均收入系统', True, YELLOW)
    pygame.draw.aaline(screen, GREEN, (1220, 80), (1780, 80), 2)  # 绘制横线 (左，上),(右，上)，粗细

    # 停车场总共收入
    textstart = xtfont.render('数据统计,现停车场总收入：' + str(int(sum_price)) + '元', True, WHITE)

    # 底部信息
    text_bottom = xtfont.render('根据数据统计分析,应多进行客户引入以及停车场项目推广！！！', True, YELLOW)

    # 获取文字图像位置
    text_re = text_title.get_rect()

    text_rect = textstart.get_rect()

    text_rect2 = text_bottom.get_rect()

    # 设置文字图像中心点
    text_re.centerx = 1500
    text_re.centery = 50

    text_rect.centerx = 1500
    text_rect.centery = 100

    text_rect2.centerx = 1500
    text_rect2.centery = 760
    # 绘制内容
    screen.blit(text_title, text_re)
    screen.blit(textstart, text_rect)
    screen.blit(text_bottom, text_rect2)

    # 加载图像
    image = pygame.image.load('interface_config/file/income.png')
    # 设置图片大小
    image = pygame.transform.scale(image, (560, 600))  # 390, 430
    # 绘制月收入表
    screen.blit(image, (1220, 130))


# 车流量统计
def text9(screen):
    # 计算price列的和
    sum_num = len(pi_info_table['carnumber'])

    # 使用系统字体
    xt1font = pygame.font.SysFont('SimHei', 24)
    xtfont = pygame.font.SysFont('SimHei', 20)
    # 表头
    text_title = xt1font.render('停车场车流量分析系统', True, YELLOW)
    pygame.draw.aaline(screen, GREEN, (1220, 80), (1780, 80), 2)  # 绘制横线 (左，上),(右，上)，粗细

    # 停车场总共收入
    textstart = xtfont.render('经数据统计,现停车场总流量为 ' + str(sum_num) + ' 个用户', True, WHITE)

    # 底部信息
    text_bottom = xtfont.render('根据数据统计分析,应多进行客户引入以及停车场项目推广！！！', True, YELLOW)

    # 获取文字图像位置
    text_re = text_title.get_rect()

    text_rect = textstart.get_rect()

    text_rect2 = text_bottom.get_rect()

    # 设置文字图像中心点
    text_re.centerx = 1500
    text_re.centery = 50

    text_rect.centerx = 1500
    text_rect.centery = 100

    text_rect2.centerx = 1500
    text_rect2.centery = 760
    # 绘制内容
    screen.blit(text_title, text_re)
    screen.blit(textstart, text_rect)
    screen.blit(text_bottom, text_rect2)

    # 加载图像
    image = pygame.image.load('interface_config/file/car.png')
    # 设置图片大小
    image = pygame.transform.scale(image, (560, 600))  # 390, 430
    # 绘制月收入表
    screen.blit(image, (1220, 130))


# 设计一个随机数，图片总列表,每次可刷新，不叠加
my_files = os.listdir("data")
listFiles = []
for files in my_files:
    if "jpg" in files:
        # print(files)
        listFiles.append(files[:-4])

# 列表随机取数
result1 = random.randint(0, len(listFiles) - 1)  # 生成 0 到 索引-1 的随机整数

data = []  # 原始索引
for i in range(len(listFiles)):
    data.append(i)


# 判断a.csv表是否为空-第1个困难
def car_iskon():
    if os.path.getsize("interface_config/datafile/停车场内.csv") == 0:
        # print("--------------------表a--------------------------")
        with open('interface_config/datafile/停车场内.csv', 'a+') as f:  # 第1次导入一个随机值防止报错
            write = csv.writer(f)
            write.writerow([result1])
        # print("--------------------表a--------------------------")

        # print("--------------------表b--------------------------")
        with open('interface_config/datafile/停车场外.csv', 'w') as f:  # 第1次导入一个随机值防止报错
            write = csv.writer(f)
            data.remove(result1)
            for j in data:
                write.writerow([j])
        # print("--------------------表b--------------------------")

    else:
        print("停车场内已有车辆，请可进行出场模拟！！！！")


# 停车场出库数据调整  出场模拟的方法
def car_out():
    with open('interface_config/datafile/停车场外.csv', 'a+') as f:  # 添加b.csv数据 回调写入方法
        write = csv.writer(f)
        write.writerow([data3[0].values[result4]])

    data7 = data3.drop(data3[data3[0].isin([data3[0].values[result4]])].index)  # 从a删除，添加到b
    with open('interface_config/datafile/停车场内.csv', 'w') as f:  # 删除a.csv数据 重新刷新覆盖
        write = csv.writer(f)
        for i in data7[0].sort_values().values:
            write.writerow([i])


# 停车场入库数据调整
def car_input():
    # 回调记录到表中解决
    with open('interface_config/datafile/停车场内.csv', 'a+') as f:  # 回调写入方法
        write = csv.writer(f)
        write.writerow([data4[0].values[result5]])

    data8 = data4.drop(data4[data4[0].isin([data4[0].values[result5]])].index)  # 从b删除，添加到a
    with open('interface_config/datafile/停车场外.csv', 'w') as f:  # 刷新覆盖
        write = csv.writer(f)
        for i in data8[0].sort_values().values:
            write.writerow([i])


clock = pygame.time.Clock()  # 游戏循环帧率设置

try:
    cam = cv2.VideoCapture(0)  # 创建摄像头实例
    print(cam.isOpened())
except:
    print('请连接摄像头')

# 执行死循环，确保窗口一直显示
while True:

    # 这里选择另一种模式通过摄像头进行识别车牌号，
    # 通过摄像头获取图片-->百度api识别车牌[更加准确]
    # sucess, img = cam.read()  # 从摄像头读取图片
    # # print(sucess)
    # cv2.imwrite('interface_config/file/test.jpg', img)  # 保存图片
    # image = pygame.image.load('interface_config/file/test.jpg')  # 加载图像
    # image = pygame.transform.scale(image, (640, 800))  # 设置图片大小
    # screen.blit(image, (2, 2))  # 绘制视频画面

    text0(screen)  # 背景和信息文字
    text1(screen)  # 表头
    text2(screen)  # 停车位信息
    text3(screen)  # 停车场信息表头
    text4(screen)  # 停车场车辆信息
    text5(screen)  # 最长停放的车辆和时间
    text6(screen, txt1, txt2, txt3, txt4)  # 在信息框中显示信息

    # 创建识别按钮
    btn.Button(screen, (150, 800), 150, 100, WHITE, BLACK, "进场模拟", 20)  # 按钮位置(左右,上下),按钮长宽,按钮高

    btn.Button(screen, (640, 800), 150, 100, WHITE, BLACK, "出场模拟", 20)  # 按钮位置(左右,上下),按钮长宽,按钮高

    # 创建车流量统计按钮
    btn.Button(screen, (1050, 790), 120, 50, GRAY, WHITE, "车流量分析", 18)  # 折线图

    # 创建收入统计按钮
    btn.Button(screen, (1180, 790), 120, 50, RED, WHITE, "日均收入分析", 18)  # 折线图

    # 不同的界面开关
    if income_switch1:
        text8(screen)
    if income_switch2:
        text9(screen)

    for event in pygame.event.get():
        # 关闭页面游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("纵横坐标轴：", str(event.pos[0]) + ',' + str(event.pos[1]))

            # 进场模拟试验
            if 0 <= event.pos[0] and event.pos[0] <= 150 and 700 <= event.pos[1] and event.pos[1] <= 800:
                # event.pos[左右范围，上下范围]
                print("现在开始进场模拟试验！！！")

                # car_data()  # 判断数据进出库
                if os.path.getsize("interface_config/datafile/停车场内.csv") == 0:
                    train = 'data'
                    img_dir = os.path.join(train, listFiles[result1] + '.jpg')
                    img_input = listFiles[result1] + '.jpg'
                    print("进场时车牌号的图片名为：", img_input)
                    # print("此次进去的索引：", result1)
                    car_iskon()  # 防止报错,填充数据

                else:
                    data4 = pd.read_csv("interface_config/datafile/停车场外.csv", header=None)  # 放置索引数1，记录停车场内的车辆
                    box1 = itemgetter(*data4[0].values)(listFiles)  # 获取对象指定域中的值，起索引到车牌转换的作用 停车场外
                    result5 = random.randint(0, len(data4[0].values) - 1)  # 对停车场外的表取进去的随机索引 即 b->a
                    # print("停车场外表的索引表b.csv：", data4[0].values)
                    # print("此次进去的索引：", result5)
                    # print("此次进去的索引对应具体值：", data4[0].values[result5])

                    car_input()  # 重新完成数据再次进库 , 防止数据的缺失

                    train = 'data'
                    img_dir = os.path.join(train, box1[result5] + '.jpg')
                    img_input = box1[result5] + '.jpg'  # 从停车场外取进去停车场的

                    # print("进场时车牌盒子:", box1)
                    # print("进场时车牌索引:", result5)
                    print("进场时车牌号的图片名为：", img_input)

                image = pygame.image.load(img_dir)

                # 设置图片大小
                image = pygame.transform.scale(image, (640, 800))
                screen.blit(image, (2, 2))
                try:
                    carnumber = get_plate_name(file_name=img_input)  # 获取识别的车牌号
                    # 另一种模式时启用
                    # carnumber = ocrutil.getcn()
                    # 格式化当前时间
                    localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())

                    carsk = pi_table['carnumber'].values  # 获取车牌号列数据
                    # 判断当前识别的车是否为停车场车辆
                    if carnumber in carsk:
                        txt1 = '车牌号: ' + carnumber
                        y = 0
                        kcar = 0
                        # 获取车辆信息
                        cars = pi_table[['carnumber', 'date', 'state']].values
                        for car in cars:
                            if carnumber == car[0]:
                                y = timeutil.DtCalc(car[1], localtime)  # 计算时间差，停车时间
                                break
                            kcar = kcar + 1
                        if y == 0:
                            y = 1
                        txt2 = '停车费： ' + str(3 * y) + '元'
                        txt3 = '出停车场时间： ' + localtime
                        # 删除此辆车的车辆信息
                        pi_table = pi_table.drop([kcar], axis=0)

                        # 更新停车场信息
                        pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                              'date': localtime,
                                                              'price': 3 * y,
                                                              'state': 1}, ignore_index=True)
                        # 保存信息更新xlsx文件
                        DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                     sheet_name='data', index=False, header=True)
                        DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                          sheet_name='data', index=False, header=True)
                        carn -= 1  # 更新停车场车辆数目

                    else:
                        # print('输出：'+str(carn))
                        if carn < Total:
                            # 添加车辆信息
                            pi_table = pi_table.append({'carnumber': carnumber,
                                                        'date': localtime,
                                                        'state': 0}, ignore_index=True)
                            # 更新xlsx文件
                            DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                         sheet_name='data', index=False, header=True)
                            if carn == Total - 1:
                                # state=0表示停车场还有车位
                                pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                                      'date': localtime,
                                                                      'state': 2}, ignore_index=True)
                            else:
                                # state=2表示停车场没有车位
                                pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                                      'date': localtime,
                                                                      'state': 0}, ignore_index=True)
                            carn += 1
                            DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                              sheet_name='data', index=False, header=True)
                            # 有停车位的提示信息
                            txt1 = '车牌号：' + carnumber
                            txt2 = '有空余车位，可以进入停车场'
                            txt3 = '进停车场时间：' + localtime
                            text7(screen, '目前还有空余车位 , 欢迎进入停车场！！！')
                        else:
                            # 没有停车位的提示信息
                            txt1 = '车牌号：' + carnumber
                            txt2 = '没有空余车位，不可以进入停车场'
                            txt3 = '时间：' + localtime
                            text7(screen, '目前已无空余车位 , 很抱歉 , 请下次再来!!!')

                except Exception as e:
                    print('错误原因：', e)
                    continue
                pass

            # 出场模拟试验
            if 480 <= event.pos[0] and event.pos[0] <= 640 and 700 <= event.pos[1] and event.pos[1] <= 800:
                # event.pos[左右范围，上下范围]
                print("现在开始出场模拟试验！！！")

                if os.path.getsize("interface_config/datafile/停车场内.csv") == 0:
                    print("停车场内暂未有车辆，请先进行进场模拟！！！！")
                    text7(screen, "停车场内暂未有车辆，请先进行进场模拟！！！！")

                else:
                    data3 = pd.read_csv("interface_config/datafile/停车场内.csv", header=None)  # 放置索引数1，记录停车场内的车辆
                    box2 = itemgetter(*data3[0].values)(listFiles)  # 获取对象指定域中的值,对索引进行转换
                    result4 = random.randint(0, len(data3[0].values) - 1)  # 随机索引 停车场内取出去的索引  即 a->b
                    # print("停车场的索引表a.csv：", data3[0].values)
                    # print("此次出去的索引：", result4)
                    # print("此次出去的索引对应具体值：", data3[0].values[result4])

                    car_out()  # 重新完成数据再次出库 , 防止数据的缺失

                    train = 'data'

                    # print("此时盒子长度为：", len(data3[0].values))

                    if len(data3[0].values) == 1:
                        img_input = box2 + '.jpg'
                        # print("出场时车牌号为:",img_input)
                    else:
                        img_input = box2[result4] + '.jpg'
                    # print("出场时车牌盒子:", box2)
                    # print("出场时车牌索引:", result4)
                    print("出场时车牌号为:", img_input)

                    img_dir = os.path.join(train, img_input)

                    image = pygame.image.load(img_dir)
                    # 设置图片大小
                    image = pygame.transform.scale(image, (640, 800))
                    screen.blit(image, (2, 2))
                    text7(screen, '停车费已缴纳,可以驶出停车场,欢迎下次光临！！！')

                    try:
                        carnumber = get_plate_name(file_name=img_input)  # 获取识别的车牌号
                        # 另一种模式时启用
                        # carnumber = ocrutil.getcn()
                        # 格式化当前时间
                        localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())

                        carsk = pi_table['carnumber'].values  # 获取车牌号列数据
                        # 判断当前识别的车是否为停车场车辆
                        if carnumber in carsk:
                            txt1 = '车牌号: ' + carnumber
                            y = 0
                            kcar = 0
                            # 获取车辆信息
                            cars = pi_table[['carnumber', 'date', 'state']].values
                            for car in cars:
                                if carnumber == car[0]:
                                    y = timeutil.DtCalc(car[1], localtime)  # 计算时间差，停车时间
                                    break
                                kcar = kcar + 1
                            if y == 0:
                                y = 1
                            txt2 = '停车费： ' + str(3 * y) + '元'
                            txt3 = '出停车场时间： ' + localtime
                            # 删除此辆车的车辆信息
                            pi_table = pi_table.drop([kcar], axis=0)

                            # 更新停车场信息
                            pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                                  'date': localtime,
                                                                  'price': 3 * y,
                                                                  'state': 1}, ignore_index=True)
                            # 保存信息更新xlsx文件
                            DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                         sheet_name='data', index=False, header=True)
                            DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                              sheet_name='data', index=False, header=True)
                            carn -= 1  # 更新停车场车辆数目

                        else:
                            # print('输出：'+str(carn))
                            if carn < Total:
                                # 添加车辆信息
                                pi_table = pi_table.append({'carnumber': carnumber,
                                                            'date': localtime,
                                                            'state': 0}, ignore_index=True)
                                # 更新xlsx文件
                                DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx',
                                                             sheet_name='data', index=False, header=True)
                                if carn == Total - 1:
                                    # state=0表示停车场还有车位
                                    pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                                          'date': localtime,
                                                                          'state': 2}, ignore_index=True)
                                else:
                                    # state=2表示停车场没有车位
                                    pi_info_table = pi_info_table.append({'carnumber': carnumber,
                                                                          'date': localtime,
                                                                          'state': 0}, ignore_index=True)
                                carn += 1
                                DataFrame(pi_info_table).to_excel(path + '停车场信息表.xlsx',
                                                                  sheet_name='data', index=False, header=True)
                                # 有停车位的提示信息
                                txt1 = '车牌号：' + carnumber
                                txt2 = '有空余车位，可以进入停车场'
                                txt3 = '进停车场时间：' + localtime
                                text7(screen, '目前还有空余车位 , 欢迎进入停车场！！！')
                            else:
                                # 没有停车位的提示信息
                                txt1 = '车牌号：' + carnumber
                                txt2 = '没有空余车位，不可以进入停车场'
                                txt3 = '时间：' + localtime
                                text7(screen, '目前没有空余车位 ,很抱歉, 请下次再来！！！')


                    except Exception as e:
                        print('错误原因：', e)
                        continue
                    pass

            # 近6天车流量统计
            if 950 <= event.pos[0] and event.pos[0] <= 1050 and 740 <= event.pos[1] and event.pos[1] <= 790:
                print('近6天车流量分析')
                if income_switch2:
                    income_switch2 = False
                    income_switch1 = True
                    size = 1200, 800
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)
                else:
                    income_switch2 = True
                    income_switch1 = False
                    size = 1800, 800  # 重新设置窗体大小
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)

                    date = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6']

                    v1 = []
                    for i in range(1, 32):
                        k = i
                        if i < 7:
                            k = '0' + str(k)
                            kk = pi_info_table[
                                pi_info_table['date'].str.contains('2023-01-' + str(k))]  # 筛选前7天数据1-1~1-7
                            kk = len(kk['carnumber'])

                            v1.append(kk)

                    print("x轴数据:", date)

                    print("y轴数据:", v1)

                    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体可以显示中文
                    # 绘制坐标轴标签
                    plt.xlabel("日期")
                    plt.ylabel("车流量")

                    plt.figure(figsize=(5.6, 6.0))  # 设置生成图片大小

                    plt.plot(date, v1, color="red", marker='o', markersize=5, label="车流量数")
                    # 设置折线图属性，date为x轴内容，v1为y轴内容相对的数据
                    # marksize用来设置'o'圆形的大小

                    plt.legend(loc="right")

                    for x1, y1 in zip(date, v1):
                        plt.text(x1, y1, '%.0f' % y1, ha='center', va='bottom', fontsize=10)
                    # x1、y1表示文本所处坐标位置，ha参数控制水平对齐方式, va控制垂直对齐方式，str(y1)表示要绘制的文本
                    plt.title('近6天车流量统计')  # 设置折线图标题
                    plt.ylim((0, max(v1) + 50))  # 设置y轴范围
                    plt.savefig('interface_config/file/car.png')  # 生成图片

            # 近6天收入统计
            if 1080 <= event.pos[0] and event.pos[0] <= 1180 and 740 <= event.pos[1] and event.pos[1] <= 790:
                print('近6天收入统计')  # 后续升级x轴轮流
                if income_switch1:
                    income_switch1 = False
                    income_switch2 = True
                    size = 1200, 800
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)
                else:
                    income_switch1 = True
                    income_switch2 = False
                    size = 1800, 800  # 重新设置窗体大小
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)

                    date = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6']

                    v1 = []
                    for i in range(1, 32):
                        k = i
                        if i < 7:
                            k = '0' + str(k)
                            kk = pi_info_table[
                                pi_info_table['date'].str.contains('2023-01-' + str(k))]  # 筛选前7天数据1-1~1-7
                            kk = kk['price'].sum()  # 计算每日的价格和
                            v1.append(kk)
                        # print(v1)

                    print("x轴数据:", date)
                    print("y轴数据:", v1)

                    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体可以显示中文
                    plt.figure(figsize=(5.6, 6.0))  # 设置生成柱状图图片大小

                    plt.bar(date, v1, 0.5, color='blue')  # 设置柱状图属性，attr为x轴内容，v1为x轴内容相对的数据
                    # 设置数字标签
                    for a, b in zip(date, v1):
                        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)
                    plt.title('近6天收入统计')  # 设置柱状图标题
                    plt.ylim((0, max(v1) + 50))  # 设置y轴范围
                    plt.savefig('interface_config/file/income.png')  # 生成图片

    pygame.display.flip()  # 更新界面
    clock.tick(FPS)  # 控制游戏最大帧率为60

# 关闭摄像头
cam.release()
