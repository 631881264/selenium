# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail():
    """邮件模块,发送邮件,带附件发送邮件"""
    def Send_Mail(self, title):
        """发送邮件
        title:邮件标题"""
        # ----------1.跟发件相关的参数------
        # 发件服务器
        smtpserver = "smtp.163.com"
        # 端口
        port = 0
        # 账号,密码(授权码)
        sender = "15355433526@163.com"
        psw = "a123456"
        # 接收人
        receiver = "631881264@qq.com"
        # ----------2.编辑邮件的内容------

        # 定义邮件正文为html格式
        body = "xxxxxxxxxxxxxx"
        msg = MIMEText(body, "html", "utf-8")
        msg['from'] = sender
        msg['to'] = "631881264@qq.com"
        msg['subject'] = title
        # ----------3.发送邮件------
        # 连服务器
        smtp = smtplib.SMTP()
        # 登录
        smtp.connect(smtpserver)
        # 发送
        smtp.login(sender, psw)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    def Send_Mail_By_File(self, file_path, title):
        """带附件发送
        title:邮件标题
        有个问题就是带汉字的邮件名没法正常显示"""
        # 发件服务器
        smtpserver = "smtp.163.com"
        # 端口
        port = 0
        # 账号,密码(授权码)
        sender = "15355433526@163.com"
        psw = "a123456"
        # 收件人
        # 如果是多个收件人
        # receiver = [邮箱,邮箱,邮箱]
        # msg["to"]=";".join(receiver)
        receiver = "631881264@qq.com"
        # ----------2.编辑邮件的内容------
        # 读文件

        with open(file_path,"r",encoding='utf-8') as fp:
            mail_body = fp.read()

        msg = MIMEMultipart("related")
        # 发件人
        msg["from"] = sender
        # 收件人                            
        msg["to"] = receiver
        # 主题
        msg["subject"] = title
        # 正文
        body = MIMEText(mail_body, "html", "utf-8")
        msg.attach(body)
        # 附件
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        # filename  指的是 附件显示的名字 跟要传递的文件交什么名字没有关系
        att["Content-Disposition"] = 'attachment; filename="report.txt"'
        msg.attach(att)
        # ----------3.发送邮件------
        # 连服务器
        smtp = smtplib.SMTP()
        # 登录
        smtp.connect(smtpserver)
        # 发送
        smtp.login(sender, psw)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
if __name__ == '__main__':
    send_mail_by_file("../report/report.txt","接口报告")



