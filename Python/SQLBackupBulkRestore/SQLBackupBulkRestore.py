#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__='Shenpf'
# PythonVersion：2.7
# *******************************************************************
# @Time    : 2018/10/11 20:24
# @Author  : shenpf
# @Email   : shen_peng_fei@126.com
# @File    : SQLBackupBulkRestore.py
# ********************************************************************

import pymssql, os, ConfigParser

# 生成config对象
conf = ConfigParser.ConfigParser()
# 用config对象读取配置文件
conf.read("SQLBackupBulkRestore.conf")

# 数据库参数变量
DBhost = conf.get("Database_Configuration", "host")
DBport = conf.get("Database_Configuration", "port")
DBuser = conf.get("Database_Configuration", "user")
DBpwd = conf.get("Database_Configuration", "password")
DataBase = conf.get("Database_Configuration", "database")

# 数据库存放路径
Storage_Path = conf.get("Path", "Storage_Path")
Storage_Path2 = conf.get("Path", "Storage_Path2")

# 数据库参数
# 数据库库名
DataBase_Name = conf.get("Database_Backup_Configuration", "DataBase_Name")
# 数据库文件
# 备份数据文件的逻辑名称
Database_Backup_Name = conf.get("Database_Backup_Configuration", "Database_Backup_Name")
# 备份数据文件的路径
File_Database = conf.get("Database_Backup_Configuration", "DataBase_File_Dir") + DataBase_Name + ".mdf"
# 数据库事务日志文件名称
File_DataLog_Name = DataBase_Name + "_log"
Database_Backup_Log_Name = conf.get("Database_Backup_Configuration", "Database_Backup_Log_Name")
# 数据库事务日志文件路径
File_Database_Log = conf.get("Database_Backup_Configuration", "DataBase_File_Dir") + File_DataLog_Name + ".ldf"
# 数据库还原事件节点
Database_Time = conf.get("Database_Backup_Configuration", "Database_Time")

# 连接MSSQL数据库
conn = pymssql.connect(host=DBhost, port=DBport, user=DBuser, password=DBpwd, database=DataBase)

# 创建数据库
# 设置自动提交
conn.autocommit(True)
sql = """
        CREATE DATABASE """ + DataBase_Name + """
        ON
        PRIMARY (NAME=""" + DataBase_Name + """,
                FILENAME = '""" + File_Database + """',
                SIZE = 100MB,
                MAXSIZE = 200,
                FILEGROWTH = 20)
        LOG ON(NAME=""" + File_DataLog_Name + """,
                FILENAME = '""" + File_Database_Log + """',
                SIZE = 10MB,
                MAXSIZE = 20,
                FILEGROWTH = 2)
        GO
      """
print(sql)
conn.autocommit(False)

# 数据库完整备份还原
conn.autocommit(True)
# 获取游标
cur = conn.cursor()
Full = os.listdir(Storage_Path + 'Full')
Full_File = Storage_Path2 + 'Full\\' + Full[-1]
Full_SQL = """
            RESTORE DATABASE """+ DataBase_Name +"""
            FROM DISK = '""" + Full_File + """'
            WITH
            move '""" + Database_Backup_Name + """'
            TO '""" + File_Database + """',
            MOVE '""" + Database_Backup_Log_Name + """'
            TO '""" + File_Database_Log + """',
            REPLACE, NORECOVERY
           """
print(Full_SQL)
cur.execute(Full_SQL)
conn.autocommit(False)

# 数据库差异备份还原
Diff = os.listdir(Storage_Path + 'Diff')
i = Diff[-len(Diff)]
for i in Diff:
    conn.autocommit(True)
    # 获取游标
    cur = conn.cursor()
    Diff_File = Storage_Path2 + 'Diff\\' + i
    Diff_SQL = """
                RESTORE DATABASE """ + DataBase_Name + """
                FROM DISK = '""" + Diff_File + """'
                WITH
                move '""" + Database_Backup_Name + """'
                TO '""" + File_Database + """',
                MOVE '""" + Database_Backup_Log_Name + """'
                TO '""" + File_Database_Log + """',
                REPLACE, NORECOVERY
               """
    print(Diff_SQL)
    cur.execute(Diff_SQL)
    conn.autocommit(False)

# 数据库事务日志备份还原
Log = os.listdir(Storage_Path + 'Log')
i = Log[-len(Log)]

for i in Log:
    conn.autocommit(True)
    # 获取游标
    cur = conn.cursor()
    # if x == -1:
    Log_File = Storage_Path2 + 'Log\\' + i
    Log_SQL = """
                    RESTORE LOG """ + DataBase_Name + """ 
                    FROM DISK = '""" + Log_File + """'
                    WITH 
                    move '""" + Database_Backup_Name + """' 
                    TO '""" + File_Database + """',
                    MOVE '""" + Database_Backup_Log_Name + """' 
                    TO '""" + File_Database_Log + """',
                    REPLACE, STOPAT = '""" + Database_Time + """'
                   """
    print(Log_SQL)
    try:
        cur.execute(Log_SQL)
        conn.autocommit(False)
    except pymssql.OperationalError, e:
        print(e)
# 关闭数据库
cur.close()
conn.close()