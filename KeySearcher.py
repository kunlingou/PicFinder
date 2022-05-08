__author__ = '雪气近'
# coding: UTF-8

import requests
import re
import time
import os


class KeySearcher:
    # 构造方法
    def __init__(self):
        print(">>>图片下载器v1.0.0<<< \r\n 图片来源：百度图片 \r\n 备注：该软件仅限交流和学习使用 \r\n author:灼华")
        self.word = input("请输入关键字: ")  # 关键字
        self.output_path = "./output/"

    # get磁盘保存路径
    @staticmethod
    def init_path(path):
        if not path.endswith("/"):
            path = path + "/"
        try:
            if os.path.exists(path):
                return path
            else:
                os.makedirs(path)
                if os.path.exists(path):
                    return path
        except FileNotFoundError:
            print('FileNotFoundError')
        raise FileNotFoundError

    # 下载图片
    def down_pic(self):
        print("download picture start")
        down_path = self.init_path(self.output_path + "picture")

        url = "https://image.baidu.com/search/flip"
        params = {'tn': 'baiduimage', 'ie': 'utf-8', 'word': self.word, 'ct': '201326592', 'ic': '0', 'lm': '-1', 'width': '', 'height': '', 'v': 'flip'}

        response = requests.get(url=url, params=params, allow_redirects=False)
        pic_url = re.findall('"objURL":"(.*?)",', response.text, re.S)

        print("正在下载中, 请耐心等待...")
        for i, each in enumerate(pic_url):
            try:
                pic = requests.get(each, timeout=10)

            except Exception as e:
                print("第" + str(i + 1) + "张：【错误】当前图片无法下载  " + str(e))
                continue
            # print("第" + str(i + 1) + "张：" + str(each))
            fp = open(down_path + str(round(time.time() * 1000)) + '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
        print("本次共下载" + str(i + 1) + "张图片，存储路径：" + down_path)

    def get_search_book(self):

        url = f"https://www.biqugesk.org/modules/article/search.php?searchkey={self.word}"
        data = requests.get(url=url, allow_redirects=False).content.decode('utf-8')

        book_list = re.findall('<tr>(.*?)</tr>', data, re.S)

        books = []

        for book in book_list:
            try:
                books.append({
                    "href": re.findall('<td class="odd"><a href="(.*?)">', book, re.S)[0],
                    "title": re.findall('<td class="odd"><a href=".*?">(.*?)</a></td>', book, re.S)[0],
                    "author": re.findall('<td class="odd">(.*?)</td>', book, re.S)[1],
                })
            except Exception as e:
                continue

        return books

    def get_book_category(self, book):

        data = requests.get(url=book["href"], allow_redirects=False).content.decode('utf-8')

        title_list = re.findall('<dd>(.*?)</dd>', data, re.S)

        category = []

        for title in title_list:
            category.append({
                "href": re.findall('<a href="(.*?)" ', title, re.S)[0],
                "title": re.findall('title="(.*?)">', title, re.S)[0]
            })
        return category

    def down_ebook(self):
        print("download book start")
        down_path = self.init_path(self.output_path + "book")

        books = self.get_search_book()

        print("books:", books)

        for book in books:
            category = self.get_book_category(book)

            full_name = f'{down_path}{book["title"]}_{book["author"]}_{str(round(time.time() * 1000))}.txt'

            fp = open(full_name, 'w', encoding='utf-8')

            for title in category:
                print(f'正在下载[{title["title"]}]......')
                try:
                    data = requests.get(url=title["href"], allow_redirects=False).content.decode('utf-8')
                    title = title["title"]
                    content = re.findall('<div class="content" id="booktext">(.*?)</div>', data, re.S)
                    content = re.findall('(.*?)<center>', content[0], re.S)
                    content = content[0].replace("&nbsp;", " ").replace("<br />", " ").encode('utf-8').decode('utf-8')
                    fp.write(title)
                    fp.write("\r\n\r\n")
                    fp.write(content)
                    fp.write("\r\n\r\n")
                except Exception as e:
                    print(f'下载失败, url = {title["href"]}, {e}')
            fp.close()
            print(f'下载完成：{full_name}')


if __name__ == "__main__":
    searcher = KeySearcher()
    searcher.down_ebook()



