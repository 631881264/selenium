import pymysql
from util import M_ini


class MyDb():

    def __init__(self,sections,style=None):
        """
        db:数据库名字
        """
        a=M_ini.MyIni("../dataconfig/DB_addr.ini")
        b=a.get_key_by_sections(sections)
        c = {}
        for i in range(len(b)):
            c[b[i][0]] = b[i][1]
        if isinstance(c["port"], str):
            c["port"] = int(c["port"])
        self.conn = pymysql.connect(**c)
        if style:
            self.cur=cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        else:
            self.cur=self.conn.cursor()


    def execute_sql(self, sql):
        """执行sql"""
        self.cur.execute(sql)

    def cur_restore(self):
        """游标归零"""
        self.cur.scroll(0, mode="absolute")

    def cur_move_relative(self,num):
        """游标相对移动"""
        self.cur.scroll(num,mode="relative")

    def cur_move_absolute(self,num):
        """游标绝对移动"""
        self.cur.scroll(num, mode="absolute")

    def get_one_result(self):
        """获取执行sql完后的第一条数据,注意
        这个函数是将游标归零后的"""
        self.cur_restore()
        return self.cur.fetchone()

    def get_all_result(self):
        """获取执行sql完后的所有数据,注意
        这个函数是将游标归零后的"""
        self.cur_restore()
        return self.cur.fetchall()

    def get_assign_result(self,num):
        """获取指定行数的结果
        num:行数"""
        self.cur_restore()
        return self.cur.fetchmany(num)
    def get_one(self):
        """获取游标下一条"""
        return self.cur.fetchone()
    def get_all(self):
        """获取游标下所有"""
        return self.cur.fetchall()
    def get_num(self,num):
        """获取游标下指定"""
        return self.cur.fetchmany()

    def conmit(self):
        """提交"""

        self.conn.commit()

    def rooback(self):
        """回滚"""
        self.conn.rollback()

    def close(self):
        """关闭"""
        self.conn.close()




if __name__ == '__main__':
    a=MyDb("mysql",style="1")
    sql="select * from student"
    a.execute_sql(sql)
    print(a.get_one())


