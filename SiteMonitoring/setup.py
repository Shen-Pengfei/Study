#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __version__ = "$Revision$"

import urllib.request
import smtplib

from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发送邮件
def E_Mail(receive,body,sender='xxxx@xx.xxx',password='xxxxxx',mailserver='smtp.exmail.qq.com',port='25'):
    """
    :param sender: 发件人邮箱
    :param password: 邮箱密码
    :param receive: 收件人邮箱
    :param body: 邮件内容
    :param mailserver: 发送邮件服务器：smtp.域名
    :param port: 发送邮件服务器端口号
    :return:
    """

    sub = 'Python3 test'  # 主题
    try:
        msg = MIMEMultipart('related')
        msg['From'] = formataddr(["Web Monitoring ", sender])  # 发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["receiver", receive])   # 收件人邮箱昵称、发件人邮箱账号
        msg['Subject'] = sub

        text = MIMEText(body, 'html', 'utf-8')
        msg.attach(text)

        smtpObj = smtplib.SMTP(mailserver, port)  # 指定发件人邮箱中的SMTP服务器，端口是25
        smtpObj.login(sender, password)  # 登陆发件人邮箱
        smtpObj.sendmail(sender, receive, msg.as_string())  # 发送邮件。发件人邮箱账号、收件人邮箱账号、发送邮件
        smtpObj.quit()
        print('success')
    except Exception as e:
        print(e)


# HTML模板
def template_html():
    haed = \
        """
    <html>
    <head>
        <meta charset='utf-8'>
        <meta http-equiv='X-UA-Compatible' content='IE=edge'>
        <title>web监控</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
    </head>"""
    body = """<body>
        <table width="400" align="center">
            <tr>
                <th>网址</th>
                <th>状态码</th>
            </tr>
    """
    bodyInfo = ''
    for i in range(len(site_list)):
        bodyInfo += '<tr>'
        bodyInfo += '<th>' + site_list[i] + '</th>'
        bodyInfo += '<th>' + str(code_list[i]) + '</th>'
        bodyInfo += '</tr>'

    html = haed + body + bodyInfo
    html += """
    </table>
    </body>
    </html>
    """
    print('HHH', html)
    return html


# 获取url code值
def check_site(url_list):
    """
    :param url_list: 传入url列表
    :return:
    """
    sites = open(url_list)
    print(type(site_list))


    for line in sites:
        # 截取网址
        site = line.strip()
        site_list.append(site)
        try:
            # 获取网页当前状态码
            response = urllib.request.urlopen(site)
            code = response.status
            code_list.append(code)
        except Exception as e:
            print(e)
    E_Mail("123456@qq.com", template_html())


if __name__ == '__main__':
    site_list = []
    code_list = []
    check_site('domain.dic')
