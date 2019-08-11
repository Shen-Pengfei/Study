#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib.request
import smtplib

from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def E_Mail(receive,body,sender='xxxx@xx.xxx',password='xxxxxx',mailserver='smtp.exmail.qq.com',port='25'):
    """
    :param sender: 发件人邮箱
    :param password: 邮箱密码
    :param receive: 收件人邮箱
    :param mailserver: 发送邮件服务器：smtp.域名
    :param port: 发送邮件服务器端口号
    :return:
    """

    sub = 'Python3 test'    # 主题
    try:
        msg = MIMEMultipart('related')
        msg['From'] = formataddr(["Web Monitoring ", sender])    # 发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["receiver", receive])   # 收件人邮箱昵称、发件人邮箱账号
        msg['Subject'] = sub

        text = MIMEText(body, 'html', 'utf-8')
        msg.attach(text)

        smtpObj = smtplib.SMTP(mailserver, port)    # 指定发件人邮箱中的SMTP服务器，端口是25
        smtpObj.login(sender, password)     # 登陆发件人邮箱
        smtpObj.sendmail(sender, receive, msg.as_string())  # 发送邮件。发件人邮箱账号、收件人邮箱账号、发送邮件
        smtpObj.quit()
        print('success')
    except Exception as e:
        print(e)


def html(url, Status_code):
    haed = """
    <!DOCTYPE html><html>
    <head>
        <meta charset='utf-8'>
        <meta http-equiv='X-UA-Compatible' content='IE=edge'>
        <title>web监控</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
    </head>
    """
    body = """
    <body>
        <table width="400" align="center">
            <tr>
                <th>网址</th>
                <th>状态码</th>
            </tr>
            <tr>
                <th>"""
    body1 = """</th><th>"""
    body2 = """</th>
            </tr>
        </table>
    </body>
    </html>
    """
    while True:
        url + Status_code
    page = haed+body
    print(page)


def check_site(url_list):
    """
    :param url: 传入url列表
    :return:
    """
    sites = open(url_list)

    site_list = []
    print(type(site_list))
    code_list = []

    for line in sites:
        # 截取网址
        site = line.strip()
        site_list.append(site)
        # print(site)
        try:
            response = urllib.request.urlopen(site)
            code = response.status
            code_list.append(code)

            # print(code)
            E_Mail("xxxx@xx.xxx", str(code))
            # print(code)
            # html(site, code)

            # E_Mail("shenpf@etlchina.net", h)
        except Exception as e:
            print(e)

    # count = 0
    # while True:
    #     if site_list[count] == site_list[-1]:
    #         # print(site_list[count])
    #         print("b")
    #         break
    #     else:
    #         print(count)
    #         print(site_list[count])
    #
    #         count = count + 1

if __name__ == '__main__':
    check_site('domain.dic')

