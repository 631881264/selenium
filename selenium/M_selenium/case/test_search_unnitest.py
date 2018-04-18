# coding:utf-8
# By: Mei
from  ddt import ddt, data, unpack
import time
from  common import M_selenium
import unittest
from page import  baidu_seach
username_passwd=[(123456,123456),(98765432,123456)]
search_value=["性能测试","自动化测试"]
@ddt
class Test_demo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """实例化page  写driver是底层要用到 """
        cls.driver=baidu_seach.baidu_page()
        cls.page=cls.driver
        cls.page.max_window()


    @data(*search_value)
    def test_search(self,data):
        """百度搜索"""
        self.page.open_url("http://www.baidu.com")
        self.page.send_value(data)
        self.page.submit()
        self.assertEqual("百度一下，你就知道",self.page.title())

    @data(*username_passwd)
    @unpack
    def test_search1(self,user,passwd):
        """百度登录"""
        self.page.open_url("http://www.baidu.com")
        self.page.click_login()
        self.page.click_username()
        self.page.send_uesrname(user)
        self.page.send_passwd(passwd)
        self.assertEqual("百度", self.page.title())
    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
