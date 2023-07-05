import os.path

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import logging
from time import sleep
import pickle
import json

logging.basicConfig(
    filename='info.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

with open('./page.json', 'r') as url:
    urls = json.load(url)

HOME_PAGE = urls['HOME_PAGE']
TARGET_PAGE = urls['TARGET_PAGE']
LOGIN_PAGE = urls['LOGIN_PAGE']


class Concert:
    def __init__(self):
        self.service = Service('./geckodriver.exe')
        self.br = webdriver.Firefox(service=self.service)
        self.status = 0
        self.login_method = 1  # {0: 模拟登录， 1： 免登录}

    def set_cookies(self):
        self.br.get(HOME_PAGE)
        print('点击登录')
        while self.br.title.find('大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！') != -1:
            sleep(1)
        print('请扫码登录！')
        while self.br.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        print('扫码成功！')
        with open('./cookies.json', 'w') as f:
            json.dump(self.br.get_cookies(), f)
        print("cookie保存成功！")
        self.br.get(TARGET_PAGE)

    def get_cookies(self):
        with open('./cookies.json', 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                self.br.add_cookie(cookie)
            print('载入cookie')

    def login(self):
        if self.login_method == 0:
            self.br.get(LOGIN_PAGE)
            print("开始登录")
        else:
            if not os.path.exists('cookies.json'):
                self.set_cookies()
            else:
                self.br.get(TARGET_PAGE)
                self.get_cookies()

    def enter_concert(self):
        print('打开浏览器，进入大麦网')
        self.login()
        self.br.refresh()
        self.status = 2
        print('登录成功')


if __name__ == "__main__":
    con = Concert()
    con.enter_concert()
