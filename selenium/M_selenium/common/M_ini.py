from configparser import ConfigParser
import os
# 初始化
# cf = ConfigParser()
# # 读取ini文件,path为要读取的ini文件的路径
# cf.read("C:/Users/my/Desktop/1.ini")
# # 获取所有sections。 即将配置文件中所有“[ ]”读取到列表中
# s = cf.sections()
# print(s)
# # 获取指定section 的配置信息
# v = cf.items("mysql")
# print(v)
#
# host=cf.get("mysql","host")
# host1=cf.getint("mysql","port")
# print(type(host))
# print(type(host1))

class MyIni():
    def __init__(self,filepath):
        self.cf=ConfigParser()
        self.cf.read(filepath,encoding="utf-8")

    def get_all_sections(self):
        """获取所有section
        section:节  被方括号包起来的叫做节"""
        return self.cf.sections()

    def get_key_by_sections(self,sections):
        """获取指定section的key值
        sections:节 格式为[xxx] 单独一行
        key: 单独一行 格式为name=value"""
        return self.cf.items(sections)

    def get_key_by_int(self,option):
        """获取指定option 返回 int形
        option: 比如数据库连接配置中的  port"""
        return self.cf.getint(option)

    def get_key_by_str(self,option):
        """获取指定option 返回str形
        option: """
        return self.cf.get(option)

    def get_key_by_bool(self,option):
        """获取指定option  返回bool形
        option: """
        return self.cf.get(option)

    def get_key_by_float(self,option):
        """获取指定option  返回float形
        option: """
        return self.cf.get(option)

    def set_option(self,section,name,value):
        """设置某个option 的值
        section:节
        需要保存
        """
        self.cf.set(section, name, value)

    def add_section(self,section):
        """添加一个section
        需要保存"""
        self.cf.add_section(section)

    def remove_option(self,section,option):
        """移除指定section下面的option
        需要保存"""
        self.cf.remove_option(section,option)

    def remove_section(self,section):
        """移除指定section
        需要保存"""
        self.cf.remove_option(section)




if __name__ == '__main__':
    AA=MyIni("../dataconfig/DB_addr.ini")
    print(AA.get_key_by_sections("mysql2"))