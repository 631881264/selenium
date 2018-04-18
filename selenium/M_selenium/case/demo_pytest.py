# # content of test_sysexit.py
from common import  M_selenium
from selenium import  webdriver
import os



import pytest
class TestSample:

   @pytest.fixture(scope="class",
                   params=["chrome","ff"])
   def dr(self,request):
       driver = M_selenium.Myselenium(request.param)
       yield driver
       driver.quit()

       # def quit(dr):
       #     dr.quit()
       # request.addfinalizer(quit(dr))

   def test_baidu(self,dr):
       dr.open("http://www.baidu.com")
       a=dr.title()
       assert a=="百度一下，你就知道"



   def test_baidu1(self,dr):
       dr.open("http://www.taobao.com")
       a = dr.title()
       assert a=="淘宝网 - 淘！我喜欢"




if __name__ == '__main__':
    pytest.main("-s -v test3.py ")







