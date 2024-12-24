#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random


def mail(mail):
    ret = True
    my_sender = "1309001246@qq.com"  # 发件人邮箱账号
    my_pass = "hghntamrvuocicje"  # 发件人邮箱密码
    code = random.randint(1000, 9999)  # 随机生成4位验证码
    try:
        msg = MIMEText(
            "您的验证码是" + str(code) + ",请不要将此告诉陌生人", "plain", "utf-8"
        )
        msg["From"] = formataddr(
            ["SCS验证官", my_sender]
        )  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg["To"] = formataddr(
            ["mail", mail]
        )  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg["Subject"] = "SCS验证码"  # 邮件的主题，也可以说是标题
        # 添加邮件内容
        server = smtplib.SMTP_SSL(
            "smtp.qq.com", 465
        )  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(
            my_sender,
            [
                mail,
            ],
            msg.as_string(),
        )  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret, code
