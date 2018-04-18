# -*- coding: utf-8 -*-
# By: Mei

from common import  M_selenium

class baidu_page(M_selenium.Myselenium):
    search_box= "id=>kw"
    submit_botton="id=>su"
    setting_text= "name=>tj_settingicon"
    login_botton="xpath=>//*[@id='u1']/a[7]"
    login_text= "css=>#TANGRAM__PSP_10__footerULoginBtn"
    username_box="name=>userName"
    passwd_box="name=>password"
    def open_url(self,url):
        self.open(url)

    def send_value(self,value):
        self.element_send(self.search_box, value)

    def submit(self):
        self.element_click(self.submit_botton)

    def click_setting(self):
        self.element_click(self.setting)

    def click_login(self):
        # self.move_to_element(self.login)
        self.element_click(self.login_botton)

    def click_username(self):
        self.element_click(self.login_text)

    def send_uesrname(self,value):
        self.element_send(self.username_box,value)

    def send_passwd(self,value):
        self.element_send(self.passwd_box,value)

    def page_title(self):
        return self.title()