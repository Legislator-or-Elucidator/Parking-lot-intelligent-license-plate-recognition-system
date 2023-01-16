from aip import AipOcr
import os


# 百度识别车牌
filename = './interface_config/file/key.txt'  # 记录申请的key的文件位置
if os.path.exists(filename):  # 判断文件是否存在
    with open(filename, "r") as file:  # 以只读方式打开文件
        dictkey = eval(file.readlines()[0])  # 读取全部内容，并且转换为字典
        APP_ID = dictkey['APP_ID']  # 获取申请的APIID
        API_KEY = dictkey['API_KEY']  # 获取申请的APIKEY
        SECRET_KEY = dictkey['SECRET_KEY']  # 获取申请的SECRETKEY
else:
    print("请先在file目录下创建key.txt")

# 初始化AipOcr对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 根据文件返回车牌号
def getcn():
    # 读取图片
    with open('interface_config/file/test.jpg', 'rb') as fp:
        image = fp.read()

    results = client.licensePlate(image)['words_result']['number']  # 调用车牌识别

    print('车牌号：' + results)  # 输出车牌号
    return results
