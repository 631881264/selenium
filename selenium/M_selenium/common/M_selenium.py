# -*- coding: utf-8 -*-
# By: Mei
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from pymouse import PyMouse


class Myselenium(object):


    original_window = None

    def __init__(self, browser="chrome"):
        """一些webdriver驱动的选择"""
        if browser == "firefox" or browser == "ff":
            profile = webdriver.FirefoxProfile()
            # 下载目录
            profile.set_preference("browser.download.dir", 'd:\\')
            # 2表示指定到目录 0桌面  1 默认
            profile.set_preference("browser.download.folderList", 2)
            # 是否显示下载器
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            # 对xx类型不提示
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip")
            driver = webdriver.Firefox(firefox_profile=profile)
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            # 修改下浏览器配置 为了下载做考虑
            options = webdriver.ChromeOptions()
            # 0 禁止弹窗  后面是 下载目录
            prefs = {"profile.default_content_settings.popups": 0, "/html/body/a[1]": "d:\\"}
            options.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(chrome_options=options)

        elif browser == "internet explorer" or browser == "ie":
            self.driver = webdriver.Ie()
        elif browser == "opera":
            self.driver = webdriver.Opera()
        elif browser == "chrome_headless":
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif browser == "edge":
            self.driver = webdriver.Edge()
        elif browser=="360":
            # 当调用谷歌内核的国内浏览器必须要查看内核版本 并保持一致
            # 自用v2.3+58内核
            # 谷歌驱动v2.3  支持内核58-60    目前360se最新版本内核是55    360chrome 9.5版本内核是63  9内核是55
            # v2.32 59-61
            # v2.33  60-62
            # v2.34  61-63
            browser_url = "C:/Users/Administrator/AppData/Roaming/360se6/Application/360se.exe"
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.binary_location = browser_url
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        else:
            raise NameError(
                "Not found %s browser,You can enter 'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'." % browser)

    def element_wait(self, by, value, secs=5):
        """
        显示等待 判断元素是否可见
        """

        if by == "id":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.ID, value)))
        elif by == "name":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.NAME, value)))
        elif by == "class":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
        elif by == "xpath":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.XPATH, value)))
        elif by == "css":
            WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            raise NoSuchElementException("Not find element, Please check the syntax error.")

    def get_element(self, css):
        """css:元素定位方式 都加上了显示等待  返回一个元素对象
        例如:  "name=>email"
        """
        if "=>" not in css:
            by = "css"
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError("Grammatical errors,reference: 'id=>useranme'.")
            self.element_wait(by, value)
        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def get_elements(self,css):
        by = css.split("=>")[0]
        value = css.split("=>")[1]

        if by == "ids":
            element = self.driver.find_elements_by_id(value)
        elif by == "names":
            element = self.driver.find_elements_by_name(value)
        elif by == "classs":
            element = self.driver.find_elements_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_elements_by_xpath(value)
        elif by == "xpaths":
            element = self.driver.find_elements_by_xpath(value)
        elif by == "csss":
            element = self.driver.find_elements_by_css_selector(value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def WebDriverWait(self,secs=5):
        return WebDriverWait(self.driver, secs, 0.5)
    #
    def alert_is_pressent(self):
        """判断是否有弹出框"""
        ele=self.WebDriverWait().until(EC.alert_is_present())
        return ele

    def element_frame(self,css):
        """判断元素是否是frame 如果是 则切进去
        css: 定位方式 "id=>kw"
        """
        ele=self.get_element(css)
        try:
            self.WebDriverWait().until(EC.frame_to_be_available_and_switch_to_it(ele))
        except:
            raise("switch to frame error  check"+css+"")

    def element_clickable(self, css):
        """判断元素是否可见可点击"""
        by = css.split("=>")[0]
        value = css.split("=>")[1]
        flag=None
        if by == "id":
            flag=self.WebDriverWait().until(EC.element_to_be_clickable((By.ID, value)))
        elif by == "name":
            flag=self.WebDriverWait().until(EC.element_to_be_clickable((By.NAME, value)))
        elif by == "class":
            flag=self.WebDriverWait().until(EC.element_to_be_clickable((By.CLASS_NAME, value)))
        elif by == "link_text":
            flag=self.WebDriverWait().until(EC.element_to_be_clickable((By.LINK_TEXT, value)))
        elif by == "xpath":
            flag= self.WebDriverWait().until(EC.element_to_be_clickable((By.XPATH, value)))
        elif by == "css":
            flag=self.WebDriverWait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, value)))
        if flag:
            return flag
        else:
            raise("元素不可点击")

    # 基本操作
    def open(self, url):
        """打开 url
        例如: driver.open("https://www.baidu.com")
        """
        self.driver.get(url)

    def url(self):
        """
        获取当前界面的url地址
        例如:driver.get_url()
        """
        return self.driver.current_url

    def title(self):
        """
        获取窗口的title
        例如:
        driver.get_title()
        """
        return self.driver.title

    def window_source(self):
        return self.driver.page_source

    def window_forward_back(self,str):
        """
        页面前进或者后退
        """
        if str =="forward":
            self.driver.forward()
        elif str == "back":
            self.driver.back()

    def F5(self):
        """刷新 例如:driver.F5()"""
        self.driver.refresh()

    def max_window(self):
        """
        窗口最大化
        例如:driver.max_window()
        """
        self.driver.maximize_window()

    def window_size(self):
        """获取窗口长宽"""
        self.driver.get_window_size()

    def window_position(self):
        """窗口坐标"""
        return self.driver.get_window_position()

    def window_rect(self):
        """获取窗口坐标以及长宽"""
        self.driver.get_window_rect()

    def set_window(self, wide, high):
        """
        设置窗口的大小
        wide:长
        high:高
        例如:driver.set_window(wide,high)
        """
        self.driver.set_window_size(wide, high)

    def close(self):
        """
        关闭浏览器
        例如:driver.close()
        """
        self.driver.close()

    def quit(self):
        """
        关闭浏览器进程
        例如:driver.quit()
        """
        self.driver.quit()

    def click_text(self, text):
        """
        根据link_text定位 并做点击操作
        例如:driver.click_text("新闻")
        """
        self.driver.find_element_by_partial_link_text(text).click()

    def wait(self, secs):
        """
        隐式等待
        例如:driver.wait(10)
        """
        self.driver.implicitly_wait(secs)

    def current_windows_screenshot(self, file_path):
        """
        当前窗口截图
        例如:driver.current_windows_screenshot()
        """
        return self.driver.get_screenshot_as_file(file_path)

    def get_screenshot_as_base64(self):
        return self.driver.get_screenshot_as_base64()

    # 窗口句柄的操作
    def current_window_handle(self):
        """获取当前窗口句柄"""
        return self.driver.current_window_handle

    def open_new_window(self, css):
        """
        如果做点击操作会打开新的界面 则切换过去
        例如:driver.open_new_window("link_text=>注册")
        """
        original_window = self.driver.current_window_handle
        el = self.get_element(css)
        el.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)

    def windows_handle_cut(self,index):
        """窗口的句柄的切换,只要需要切换到第几个窗口即可
        例如:driver.window_han(0)"""

        all_handle=self.driver.window_handles
        self.driver.switch_to.window(all_handle[index])



    # 弹出框操作
    def alert_text(self):
        """获取一个弹出框的文本值 这个地方加了一个窗口的切换  防止windows弹窗"""
        flag=None
        try:
            ele=self.alert_is_pressent()
            flag= ele.text
        except:
            try:
                alert = Alert(self.driver)
                flag= alert.text
            except:
                try:
                    self.windows_handle_cut(index=1)
                    self.alert_text()
                except:
                    raise("not find alert")
        return flag

    def alert_accept(self):
        """弹出框的确定"""
        try:
            ele=self.alert_is_pressent()
            ele.accept()
        except:
            try:
                alert = Alert(self.driver)
                alert.accept()
            except:
                raise("not find alert")

    def alert_dismiss(self):
        """弹出框的取消"""
        try:
            ele=self.alert_is_pressent()
            ele.dismiss()
        except:
            try:
                alert = self.driver.switch_to_alert()
                alert.dismiss()
            except:
                try:
                    alert = Alert(self.driver)
                    alert.dismiss()
                except:
                    raise ("not find alert")

    def alert_sendkeys(self,string):
        """在弹出框中输入内容"""
        try:
            ele=self.alert_is_pressent()
            ele.send_keys(string)
        except:
            try:
                alert = self.driver.switch_to_alert()
                alert.send_keys(string)
            except:
                try:
                    alert = Alert(self.driver)
                    alert.send_keys(string)
                except:
                    raise ("not find alert")

    # 元素的click send submit clear doub

    def element_click(self, css):
        """
        元素定位并且做点击操作
        例如:driver.click("id=>kw")
        """
        ele=self.get_element(css)
        ele.click()

    def element_send(self, css, text):
        """
        元素定位并且输入
        例如:driver.type("id=>kw","ui自动化")
        """
        ele = self.get_element(css)
        ele.send_keys(text)

    def element_send_submit(self,css,value):
        """输入并提交"""
        self.element_send(css,value)
        self.element_submit(css)

    def element_submit(self, css):
        """
        定位元素并且提交
        例如:driver.submit("id=>su")
        """
        ele= self.get_element(css)
        ele.submit()

    def element_clear(self, css):
        """
        元素定位且清空输入
        例如:driver.clear("id=>kw")
        """
        ele = self.get_element(css)
        ele.clear()

    # 奇奇怪怪的鼠标事件 左键双击 单击右键  拖拽
    def element_right_click(self, css):
        """
        在某个元素上进行鼠标右击
        例如:driver.right_click("id=>kw")
        """
        ele = self.get_element(css)
        ActionChains(self.driver).context_click(ele).perform()

    def move_to_element(self, css):
        """
        鼠标悬停
        例如:driver.move_to_element("css=>#el")
        """
        ele = self.get_element(css)
        ActionChains(self.driver).move_to_element(ele).perform()

    def element_double_click(self, css):
        """
        元素双击操作
        例如:driver.double_click("css=>#el")
        """
        ele = self.get_element(css)
        ActionChains(self.driver).double_click(ele).perform()

    def drag_and_drop(self, el_css, ta_css):
        """
        元素拖动
        el_css:起始元素
        ta_css:目标位置
        例如:driver.drag_and_drop("css=>#el","css=>#ta")
        """
        element = self.get_element(el_css)
        target = self.get_element(ta_css)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    #  键盘事件 摒弃 key_down key_up 这套
    def key(self,css,value):
        """键盘的删除 空格 tab esc"""
        if value=="back":
            self.get_element(css).send_keys(Keys.BACK_SPACE)
        elif value=="space":
            self.get_element(css).send_keys(Keys.SPACE)
        elif value=="tab":
            self.get_element(css).send_keys(Keys.TAB)
        elif value=="esc":
            self.get_element(css).send_keys(Keys.ESCAPE)

    def keys(self,css,value):
        """control+value  比如 a c v x"""
        self.get_element(css).send_keys(Keys.CONTROL,value)


    # 疑难问题上js
    def js(self, script):
        """
        执行js
        例如:driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)

    def scrollbar(self,left,top):
        """滚动条的操作
        left:距离最左边距离
        top:距离最上边距离"""
        js = "window.scrollTo("+str(left)+","+str(top)+");"
        self.js(js)

    def remove_readonly(self,id):
        """
        当元素有唯一的id属性 并且需要移除readonly时候 可以用这个函数
        一般用在日期控件上,但是需要注意的是  必须要先clear 再send
        移除readonly属性
        或者用.readonly=false
        肯定是先要定位到具体的
        """
        js2="document.getElementById('"+id+"').removeAttribute('readonly')"
        self.js(js2)

    def get_attribute_inner(self,css):
        """获取某个元素的innerHtml属性"""
        ele=self.get_element(css)
        return  ele.get_attribute("innerHTML")

    # frame的操作
    def switch_to_frame(self, css):
        """
        切入frame
        例如:driver.switch_to_frame("id=>kw")
        需要注意的是 frame结构 需要层层切入  例如
        一个frame嵌套一个frame  则去要层层切入
        """
        try:
            self.element_frame(css)
        except:
            try:
                iframe_ele = self.get_element(css)
                self.driver.switch_to.frame(iframe_ele)
            except:
                raise("switch to frame error  check"+css+"")

    def switch_to_frame_up(self):
        """切换到上一层frame"""
        self.driver.switch_to.parent_frame()

    def switch_to_frame_out(self):
        """
        退出frame 结束表单操作
        例如:driver.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()

    def element_display(self, css):
        """
        判断元素是否可见
        例如:driver.get_display("id=>kw")
        """
        ele = self.get_element(css)
        return ele.is_displayed()

    def element_enabled(self,css):
        """判断元素是否可操作
        例如:driver.get_enabled("id=>kw")
        """
        ele=self.get_element(css)
        return ele.is_enabled()

    # 表格的验证 共多少行  多少列  每行每列数据
    def table_count_col(self,css):
        """表格多少列"""
        ele=self.get_elements(""+css+"/tr[1]/td")
        return len(ele)

    def table_count_row(self,css):
        """表格多少行"""
        ele=self.get_elements(""+css+"/tr")
        return len(ele)

    def table_cell_value(self,css,row,col):
        """
        获取指定单元格数据
        row:行
        col:列
        定位到table即可"""
        return self.get_element(""+css+"/tr["+str(row)+"]/td["+str(col)+"]").text

    def table_row_values(self,css,row):
        """获取table一行数据"""
        num=self.table_row(css)
        row_list=[]
        ele = self.get_elements("" + css + "/tr["+str(row)+"]")
        for i in ele:
            value=i.text
        a=value.split(" ")
        return a

    def table_col_values(self,css,col):
        """获取表格一列数据"""
    #    先获取一行数据  再获取所有行数据  根据 每行的下标取值
    #   num table的所有行
        num=self.table_row(css)
        all_col_values=[]
        # 下面需要注意实际行数是从1开始  而不是0  所以 所以用num+1 而不是num
        for i in range(1,num+1):
            all_row_values=self.table_row_values(css,i)
            # 下面这个是因为输入的列是从1开始  但是列表下标是从0开始
            num1=col-1
            all_col_values.append(all_row_values[num1])
        return all_col_values


    # 下拉框 单选 复选   单/多行 点击 取消 返回text
    def select_click(self, css, value):
        """
        下拉框的点击操作  value 为:行(0为起始行 注意了 ) text value值 都行
        """
        ele = self.get_element(css)
        if isinstance(value,str):
            try:
                Select(ele).select_by_value(value)
            except:
                Select(ele).select_by_visible_text(value)
        elif isinstance(value,int):
            Select(ele).select_by_index(value)

    def select_all_optinon(self,css):
        """获取所有select的option 方便下面做遍历"""
        return Select(self.get_element(css)).options

    def select_all_text(self,css):
        """下拉的所有text"""
        all_options=self.select_all_optinon(css)
        all_text=[]
        for i in all_options:
            all_text.append(i.text)
        return all_text

    def select_circulation_click(self,css):
        """对下拉框挨个点击 并返回text值"""
        ele=self.select_all_optinon(css)
        select_all_value=[]
        for select in ele:
            select.click()
            select_all_value.append(select.text)
        return select_all_value

    def select_uclick(self,css,value):
        """取消单行选中"""
        ele = self.get_element(css)
        if isinstance(value, str):
            try:
                Select(ele).deselect_by_value(value)
            except:
                Select(ele).deselect_by_visible_text(value)
        elif isinstance(value, int):
            Select(ele).deselect_by_index(value)

    def select_more_uclick(self,css,*value):
        """取消多行选中"""
        ele = self.get_element(css)
        for i in range(len(value)):
            Select(ele).deselect_by_index(value[i])

    def select_more_click(self,css,*value):
        """选中多行 并返回text"""
        ele = self.get_element(css)
        # 先去的所有value值  然后 通过传进来的参数 取相应的数据
        all_value=self.select_all_text(css)
        more_value=[]
        for i in range(len(value)):
            Select(ele).select_by_index(value[i])
            print(value[i])
            more_value.append(all_value[value[i]])
        return more_value

    def select_all_uclick(self,css):
        """取消所有行选中"""
        ele = self.get_element(css)
        Select(ele).deselect_all()

    # 上传/下载基于坐标 下载修改了webdriver的配置
    def send_file(self,x,y,x1,y1):
        """上传 基于坐标 拿尺子量坐标吧 .."""
        m = PyMouse()
        m.click(x,y)
        m.click(x1,y1)

    # cookies相关
    def get_cookies(self):
        """获取所有cookie"""
        self.driver.get_cookies()

    def get_cookie_name(self,name):
        """获取指定name的cookie"""
        self.driver.get_cookie(name)

    def add_cookie(self,**cookies):
        """添加cookie
        例如:driver.add_cookie(a=b,c=d)"""

        self.driver.add_cookie(**cookies)

    def del_cookie(self,name):
        """删除指定cookie"""
        self.driver.delete_cookie(name)

    def del_all_cookie(self):
        """删除所有cookies"""
        self.driver.delete_all_cookies()

    # 元素的一些判断
    def element_clickable(self, css, secs=5):
        """判断元素是否可见可操作"""
        by = css.split("=>")[0]
        value = css.split("=>")[1]
        if by == "id":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.ID, value)))
        elif by == "name":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.NAME, value)))
        elif by == "class":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, value)))
        elif by == "link_text":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.LINK_TEXT, value)))
        elif by == "xpath":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.XPATH, value)))
        elif by == "css":
                WebDriverWait(self.driver, secs, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, value)))
        else:
            raise NoSuchElementException(
                "Not find element, Please check the syntax error.")

    def element_is_selectd(self,css):
        """查看元素是否被选中"""
        return self.get_element(css).is_selected()

    def element_is_displayed(self,css):
        """查看元素是否隐藏"""
        return self.get_element(css).is_displayed()

    def element_is_enabled(self,css):
        """判断元素是否可以操作"""
        return self.get_element(css).is_enabled()

    def element_html(self,css,str):
        """获取元素的基本信息如text tagname size"""
        flag=None
        if str=="text":
            flag=self.get_element(css).text
        elif  str=="tag":
            flag=self.get_element(css).tag_name
        elif str=="size":
            flag=self.get_element(css).size
        if flag:
            return flag
        else:
            raise("str must be text,tag,size")

    def element_attribute(self,css,str):
        """获取元素属性值 比如 id name  value"""
        flag=self.get_element(css).get_attribute(str)
        if flag:
            return flag
        else:
            raise("str must be id,name,value... ")

    def element_css(self,css,value):
        """获取元素样式 例如font  height width  这个地方底层没有错误返回"""
        return self.get_element(css).value_of_css_property(value)

    def element_message(self,css,str):
        """获取元素内所有信息 只要给个关键词 无论标签还是属性或者是css样式 """
        flag=None
        try:
            flag=  self.element_message(css, str)
        except:
            try:
                flag= self.element_attribute(css, str)
            except:
                flag=self.element_css(css,str)
        return flag



















if __name__ == '__main__':
    driver = Pyse("chrome")
