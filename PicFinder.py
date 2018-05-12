__author__ = '雪气近'
# coding: UTF-8


import requests
import re
import time
import os

class PicFinder:
    # 构造方法
    def __init__(self):
        print(">>>图片下载器v1.0.0<<< \r\n 图片来源：百度图片 \r\n 备注：该软件仅限交流和学习使用 \r\n author:雪气近")
        word = input("请输入关键字(Input key word): ")  # 关键字
        self.url = "https://image.baidu.com/search/flip"
        self.params = {'tn': 'baiduimage', 'ie': 'utf-8', 'word': word, 'ct': '201326592', 'ic': '0', 'lm': '-1', 'width': '', 'height': '', 'v': 'flip'}
        self.down_pic()

    # get 图片下载地址
    def get_pic_url(self):
        response = requests.get(url=self.url, params=self.params, allow_redirects=False)
        # print(response.url)
        return response.text

    # get磁盘保存路径
    @staticmethod
    def down_path():
        for down_path in ('E:/PicFinder/pictures/', 'E:/', 'D:/PicFinder/pictures/', 'C:/PicFinder/pictures/'):
            try:
                if os.path.exists(down_path):
                    break
                else:
                    os.makedirs(down_path)
                    if os.path.exists(down_path):
                        break
            except FileNotFoundError:
                continue
            if down_path == 'C:/':
                print('无法找到合法的存储路径，请联系管理员！')
                return 0
        return down_path

    # 下载图片
    def down_pic(self):
        down_path = self.down_path()
        if down_path == 0:
            return
        pic_url = re.findall('"objURL":"(.*?)",', self.get_pic_url(), re.S)  # 正则表达式

        i = 0
        for each in pic_url:
            # print(each)
            try:
                pic = requests.get(each, timeout=10)

            except Exception as e:
                print("第" + str(i + 1) + "张：【错误】当前图片无法下载  " + str(e))
                continue
            print("第" + str(i + 1) + "张：" + str(each))
            string = down_path + str(round(time.time() * 1000)) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
            # if i == 5:
            #     break
        print("存储路径：" + down_path)
        print("本次共下载" + str(i) + "张图片")
run = True
while run:
    PicFinder()
    os.system("pause")
    if input("是否继续？'否'请按回车键；'是'请输入任何字符，并回车键结束: ") == "":
        run = False



