import time
from io import BytesIO
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from os.path import abspath, dirname

TEMPLATES_FOLDER = dirname(abspath(__file__)) + '/templates/'


class WebCookies():
    def __init__(self, username, browser):
        self.url = 'https://v.sogou.com/'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        # self.password = password
    
    def open(self):
        """
        打开网页
        :return: None
        """
        self.browser.get(self.url)
        time.sleep(1)

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()
    
    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        cookies = self.get_cookies()
        return {
            'status': 1,
            'content': cookies
        }


if __name__ == '__main__':
    result = WebCookies('14773427930', 'x6pybpakq1').main()
    print(result)
