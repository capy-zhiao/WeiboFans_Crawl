import os
import json


class CookieLogin:
    def __init__(self, f_path):
        """
        :param url: 首页地址
        :param f_path: Cookies文件保存路径
        """
        self.f_path = f_path

    def save_cookies(self, data, encoding="utf-8"):
        """
        :param data: 所保存数据
        :param encoding: 文件编码,默认utf-8
        """
        with open(self.f_path, "w", encoding=encoding) as f_w:
            json.dump(data, f_w)
        print("saved!")

    def load_cookies(self, encoding="utf-8"):
        """
        Cookies读取方法
        :param encoding: 文件编码,默认utf-8
        """
        if os.path.isfile(self.f_path):
            with open(self.f_path, "r", encoding=encoding) as f_r:
                user_cookies = json.load(f_r)
            return user_cookies
