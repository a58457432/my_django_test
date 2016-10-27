#!/bin/env python
#-*-coding:utf-8-*-

import MySQLdb
import string
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.header import Header

def get_item(data_dict,item):
    try:
       item_value = data_dict[item]
       return item_value
    except:
       return '-1'

def get_config(group,config_name):
    config = ConfigParser.ConfigParser()
    config.readfp(open('./myapp/etc/config.ini','r'))
    #config.readfp(open('../etc/config.ini','r'))
    config_value=config.get(group,config_name).strip(' ').strip('\'').strip('\"')
    return config_value

def filters(data):
    return data.strip(' ').strip('\n').strip('\br')

host = get_config('monitor_server','host')
port = get_config('monitor_server','port')
user = get_config('monitor_server','user')
passwd = get_config('monitor_server','passwd')
dbname = get_config('monitor_server','dbname')
def mysql_exec(sql,param):
    try:
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
        conn.select_db(dbname)
        curs = conn.cursor()
        if param <> '':
            curs.execute(sql,param)
        else:
            curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception,e:
       print "mysql execute: " + str(e)


def mysql_query(sql):
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
    conn.select_db(dbname)
    cursor = conn.cursor()
    count=cursor.execute(sql)
    index=cursor.description
    col=[]
    for i in index:
        col.append(i[0])
    result=cursor.fetchall()
    return (result,col)
    cursor.close()
    conn.close()

def main():
    result=mysql_query('select *  from db_servers_mysql;')
if __name__=='__main__':
    main()