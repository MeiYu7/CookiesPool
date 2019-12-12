import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookiespool.config import *
from cookiespool.db import RedisClient
from cookiespool.cookies import WebCookies
import time


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps,
                                               executable_path=r'F:/PhantomJs/phantomjs-2.1.1-windows/bin/phantomjs.exe')
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            # Chrome浏览器
            options = webdriver.ChromeOptions()
            # 设置中文
            options.add_argument('lang=zh_CN.UTF-8')
            # 设置无图加载 1 允许所有图片; 2 阻止所有图片; 3 阻止第三方服务器图片
            prefs = {'profile.default_content_setting_values': {'images': 2}}
            options.add_experimental_option('prefs', prefs)
            # 设置无头浏览器
            # options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=options, executable_path="F:/ChromeDriver/chromedriver.exe")

    def new_cookies(self, username):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行, 虚拟登录
        :return:
        """
        time_username = time.strftime('%Y%m%d%H%M%S', time.localtime())
        print('正在生成Cookies', '时间账号', time_username)
        result = self.new_cookies(time_username)
        # 成功获取
        if result.get('status') == 1:
            cookies = self.process_cookies(result.get('content'))
            print('成功获取到Cookies', cookies)
            if self.cookies_db.set(time_username, json.dumps(cookies)):
                print('成功保存Cookies')

    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class SogouCookiesGenerator(CookiesGenerator):
    def __init__(self, website='sogou'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return WebCookies(username, self.browser).main()


if __name__ == '__main__':
    generator = SogouCookiesGenerator()
    generator.run()
