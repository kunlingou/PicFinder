# coding: UTF-8
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from fast_zip import *


class MainQWidget:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setGeometry(300, 300, 300, 220)
        self.widget.setWindowTitle('FastTool')

        btn = QPushButton('zip解密', self.widget)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(self.button_clicked)
        pass

    def show(self):
        self.widget.show()

    @staticmethod
    def button_clicked():
        print("zip解密 点击")
        fast_unzip2("书籍测试.zip", "123456")
        pass


def main():
    app = QApplication(sys.argv)
    widget = MainQWidget()
    widget.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    main()

