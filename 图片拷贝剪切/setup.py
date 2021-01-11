#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Python Version：2.7


import os,logging.handlers
import datetime,time, ConfigParser
import chardet

# 如果迁移成功，写入log文件。未成功写入WARNING文件
# 获取开始时间
begin = datetime.datetime.now()

# 打开路径文件
# Root = open("Text")

# 通过logging.basicConfig函数对日志的输出格式及方式做相关配置
"""
filename ：日志文件的保存路径。如果配置了些参数，将自动创建一个FileHandler作为Handler；
filemode ：日志文件的打开模式。 默认值为'a'，表示日志消息以追加的形式添加到日志文件中。如果设为'w', 那么每次程序启动的时候都会创建一个新的日志文件；
format ：设置日志输出格式；
datefmt ：定义日期格式；
level ：设置日志的级别.默认为WARNING.CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET;对低于该级别的日志消息将被忽略；
stream ：设置特定的流用于初始化StreamHandler；
"""

log_warning = r"log/" + time.strftime("%Y%m%d%H%M%S")+"warning.log"
LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s"
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S"
handler = logging.handlers.RotatingFileHandler(log_warning, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler

logging.basicConfig(level=logging.WARNING,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=log_warning,       # 日志文件路径及名字
                    filemode='w')

# 生成config对象
conf = ConfigParser.ConfigParser()
# 用config对象读取配置文件
conf.read(r"etc/Pic-python2.7.conf")

# 路径文件
Source_file_Name = conf.get("File_Old","Source_file_Name")
print(Source_file_Name)

# 源路径
Old_File_Path = conf.get("File_Old", "Old_File_Path")
# 迁移路径
File_Path_New = conf.get("File_New", "File_Path_New")
# 打开所读取的文件
Source_file = open(Source_file_Name)

# 计数器
i = 0
x = 0

# 判断文件的编码格式
data = chardet.detect(Source_file.read())['encoding']

# 如果文件编码为ascii，则执行
if data == 'ascii':

    # 取出Root的每行数据
    Root_lines = Source_file.readlines()
    for Root_line in Root_lines:
        Root_line = Root_line.strip()

        # 原路径
        File_Old = Old_File_Path + Root_line
        # 迁移路径
        File_New = File_Path_New + Root_line

        # 截取文件目录路径
        father_path = os.path.abspath(os.path.dirname(File_New) + os.path.sep + ".")
        if not os.path.exists(father_path):
            os.makedirs(father_path)
        try:
            os.rename(File_Old, File_New)
            # print >> print_file, "第%s条数据:" % i + File_Old + "迁移成功"
            x = x + 1
        except:
            logging.warning("这是第%s条数据，读取内容为：%s" % (i, Root_line))
            print("\033[5;30m这是第%s条数据，读取内容为：%s\033[0m" % (i, Root_line))
            i = i + 1
else:
    print("此文件的编码格式为：%s，请转换成ASCII编码格式文件！" %(data))

# 关闭文件
Source_file.close()
# 获取结束时间
end = datetime.datetime.now()
# 计算运行时间
Runtime = (end - begin).total_seconds()
mins = Runtime%60
print("脚本运行时间为：" + str(Runtime//60) + "分" + str(Runtime%60) + "秒")
print("迁移成功%s条数据，不成功%s条数据……" % (x,i))

