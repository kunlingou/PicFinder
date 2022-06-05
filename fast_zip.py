# coding: UTF-8
import zipfile
import pyzipper
import time
import threading

g_start = 0
g_finish = 0
MAX_THREAD_NUM = 16
VAL = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
VAL2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '_']


class PasswordIter:
    def __init__(self, length):
        self.len = length
        self.pwd = [0 for _ in range(length)]
        self.end = 0
        self.max_val = len(VAL) - 1
        pass

    def next(self):
        if self.end:
            return None
        pwd_str = "".join([VAL[i] for i in self.pwd])
        self.pwd[self.len - 1] += 1
        for i in range(self.len - 1, -1, -1):
            if self.pwd[i] > self.max_val:
                if i <= 0:
                    self.end = 1
                    print(f"go to end {pwd_str}")
                    return None
                self.pwd[i] -= self.max_val
                self.pwd[i - 1] += 1
        return pwd_str


def extract(thread_no, zip_file, pwd_len):
    global g_finish
    print(f"extract start ,thread_no = {thread_no} pwd_len = {pwd_len}")
    pwd_iter = PasswordIter(pwd_len)
    i = -1
    fail = 0
    while 1:
        if g_finish != 0:
            return
        pwd = pwd_iter.next()
        if not pwd:
            print(f"get next fail,thread_no = {thread_no}")
            return
        i += 1
        if (i % MAX_THREAD_NUM) != thread_no:
            continue
        try:
            zip_file.extractall(path='.', pwd=pwd.encode('utf-8'))
        except Exception as e:
            if fail % 1000 == 0:
                print(f"try extractall err ,password = {pwd} thread_no = {thread_no} time = {time.time() - g_start} {e}")
            fail += 1
            continue
        now = time.time()
        print("the password is {}".format(pwd))
        print("spend time is {}".format(now - g_start))
        g_finish = 1
    pass


def fast_unzip(file_name, pwd_len):
    global g_start, g_finish
    g_start = time.time()
    g_finish = 0
    zip_file = pyzipper.AESZipFile(file_name, 'r', compression=pyzipper.ZIP_DEFLATED,
                                   encryption=pyzipper.WZ_AES)
    threads = []
    for thread_no in range(MAX_THREAD_NUM):
        t = threading.Thread(target=extract, args=(thread_no, zip_file, pwd_len))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    if g_finish:
        print("解压成功")
    else:
        print("解压失败")


def fast_unzip2(file_name, pwd):
    zip_file = pyzipper.AESZipFile(file_name, 'r', compression=pyzipper.ZIP_DEFLATED,
                                   encryption=pyzipper.WZ_AES)
    try:
        zip_file.extractall(path='.', pwd=pwd.encode('utf-8'))
    except Exception as e:
        print(e)
        print("解压失败")
        return
    print("解压成功")
    pass


def fast_unzip3(file_name, pwd):
    try:
        with pyzipper.AESZipFile(file_name, 'r', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as extracted_zip:
            extracted_zip.extractall(pwd=pwd.encode('utf-8'))
    except Exception as e:
        print(e)
        print("解压失败")
        return
    print("解压成功")


if __name__ == "__main__":
    fast_unzip("算法导论.zip", 5)
