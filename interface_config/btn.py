# coding=utf-8
import pygame


# 自定义按钮
class Button():
    # msg为要在按钮中显示的文本
    def __init__(self, screen, centerxy, width, height, button_color, text_color, msg, size):
        ''' 初始化按钮的属性 '''
        self.screen = screen
        self.width, self.height = width, height  # 设置按钮的宽和高
        self.button_color = button_color  # 设置按钮的rect对象颜色为深蓝
        self.text_color = text_color  # 设置文本的颜色为白色

        # 1.设置文本字体与大小
        self.font = pygame.font.SysFont('SimHei', size)
        # 2.设置按钮大小
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 3.创建按钮的rect对象，并设置按钮的中心位置
        self.rect.centerx = centerxy[0] - self.width / 2 + 2
        self.rect.centery = centerxy[1] - self.height / 2 + 2
        # 4.填充颜色
        self.screen.fill(self.button_color, self.rect)

        # 渲染图像
        self.deal_msg(msg)

    def deal_msg(self, msg):
        '''将msg渲染为图像，并将其在按钮上居中'''
        # 5.将文本写到按钮上
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)
        # 6.设置文本在按钮上的位置：文本的中心就是按钮的中心（即文本居中）
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center
        # 7.绘制到屏幕上
        self.screen.blit(self.msg_img, self.msg_img_rect)
