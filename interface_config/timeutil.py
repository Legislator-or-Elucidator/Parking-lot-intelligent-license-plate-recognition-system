# coding=utf-8
import datetime


# 计算停车时间四舍五入
def DtCalc(stTime, edTime):
    st = datetime.datetime.strptime(stTime, "%Y-%m-%d %H:%M")
    ed = datetime.datetime.strptime(edTime, "%Y-%m-%d %H:%M")
    rtn = ed - st
    y = round(rtn.total_seconds() / 60 / 60)
    return y


# 返回星期几标记0代表星期一，1代表星期二   6代表星期天
def get_week_number(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    day = date.weekday()
    return day
