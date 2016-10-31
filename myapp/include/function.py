#!/bin/env python
#-*-coding:utf-8-*-
import MySQLdb,sys,string,time,datetime
from django.contrib.auth.models import User
from myapp.models import Db_name,Db_account,Db_instance

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


def mysql_query(sql,user=user,passwd=passwd,host=host,port=int(port),dbname=dbname):
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

#获取下拉菜单列表
def get_mysql_hostlist(username):
    a = User.objects.get(username=username)
    host_list=[]
    #如果没有对应role='read'或者role='all'的account账号，则不显示在下拉菜单中
    for row in a.db_name_set.all():
        if row.db_account_set.all().exclude(role='write'):
            host_list.append(row.dbtag)
    return host_list


def get_mysql_data(hosttag,sql):
    #确认dbname
    a = Db_name.objects.filter(dbtag=hosttag)[0]
    #a = Db_name.objects.get(dbtag=hosttag)
    tar_dbname = a.dbname
    #如果instance中有备库role='read'，则选择从备库读取
    try:
        if a.instance.all().filter(role='read')[0]:
            tar_host = a.instance.all().filter(role='read')[0].ip
            tar_port = a.instance.all().filter(role='read')[0].port
    #如果没有设置或没有role=read，则选择第一个库读取
    except Exception,e:
        tar_host = a.instance.all()[0].ip
        tar_port = a.instance.all()[0].port
    for i in a.db_account_set.all():
        if i.role!='write ':
            tar_username = i.user
            tar_passwd = i.passwd
    #print tar_port+tar_passwd+tar_username+tar_host
    results,col = mysql_query(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname)
    return results,col,tar_dbname

#检查输入语句
def check_mysql_query(sqltext,user):
    #根据user确定能够select 的行数
    try :
        num = User.objects.get(username=user).user_profile.select_limit
    except Exception, e:
        num = 200
    limit = ' limit '+str(num)

    sqltext = sqltext.strip().lower()
    sqltype = sqltext.split()[0]
    list_type = ['select','show','desc']
    #flag 1位有效 0为list_type中的无效值
    flag=0
    while True:
        sqltext = sqltext.strip()
        lastletter = sqltext[len(sqltext)-1]
        if (not cmp(lastletter,';')):
            sqltext = sqltext[:-1]
        else:
            break
    has_limit = cmp(sqltext.split()[-2],'limit')
    for i in list_type:
        if (not cmp(i,sqltype)):
            flag=1
            break
    if (flag==1):
        if (sqltype =='select' and has_limit!=0):
            return sqltext+limit
        else:
            return sqltext
    else:
        return "ERROR"



def main():
    return 1
if __name__=='__main__':
    main()