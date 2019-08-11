#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2019/4/24 12:12
# PythonVersion：3.6

import os
import xlwt
import xml.etree.ElementTree as ET

"""
Execl文件写入
"""
def write_excel_xls(file_excel_path, sheet_name, value):
    """
    :param file_excel_path: excel存放路径及名称
    :param sheet_name: sheet表名称
    :param value:传入读取xml数据
    :return:
    """
    index = len(value)
    # 新建一个Excel
    book = xlwt.Workbook()
    # 新建一个sheet页
    sheet = book.add_sheet(sheet_name)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])
    book.save(file_excel_path)
    print("xls格式表格写入数据成功！")

"""
xml文件读取
"""
def read_xml(file_xml_path ):
    """
    :param file_xml_path: xml文件存放路径及名称
    :return:
    """
    xmlfilepath = os.path.abspath(file_xml_path)
    print("xml文件路径：", xmlfilepath)

    # 得到文档对象
    domobj = ET.parse(xmlfilepath)
    # 获取根元素
    root = domobj.getroot()
    # 获取列表
    for child in root:
        lists.append(
            [child.attrib['SITE.NAME'], child.attrib['SITE.ID'], child.attrib['bindings'], child.attrib['state']]
        )
    print(lists)

if __name__=='__main__':
    lists = [['站点', 'ID', '网址', '状态'],]
    # xml文件配置
    file_xml_path = r"xmlfile\test.xml"
    read_xml(file_xml_path)

    # Excel文件配置
    book_name_xls = 'xls格式测试工作簿.xls'
    sheet_name_xls = 'xls格式测试表'
    write_excel_xls(book_name_xls, sheet_name_xls, lists)



