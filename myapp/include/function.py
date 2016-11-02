#!/bin/env python
#-*-coding:utf-8-*-
import MySQLdb,sys,string,time,datetime
from django.contrib.auth.models import User
from myapp.models import Db_name,Db_account,Db_instance,Oper_log

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

host = get_config('settings','host')
port = get_config('settings','port')
user = get_config('settings','user')
passwd = get_config('settings','passwd')
dbname = get_config('settings','dbname')
select_limit = int(get_config('settings','select_limit'))
wrong_msg = get_config('settings','wrong_msg')

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
    #result=cursor.fetchall()
    result=cursor.fetchmany(size=1000)
    return (result,col)
    cursor.close()
    conn.close()

#获取下拉菜单列表
def get_mysql_hostlist(username,tag='tag'):
    host_list=[]
    if (tag=='tag'):
        a = User.objects.get(username=username)
        #如果没有对应role='read'或者role='all'的account账号，则不显示在下拉菜单中
        for row in a.db_name_set.all():
            if row.db_account_set.all().exclude(role='write'):
                host_list.append(row.dbtag)
    elif (tag=='log'):
        for row in Db_name.objects.values('dbtag').distinct():
            host_list.append(row['dbtag'])
    return host_list

def get_op_type(methods='get'):
    #all表示所有种类
    op_list=['all','truncate','drop','create','delete','update','insert','select','explain','create','show']
    if (methods=='get'):
        return op_list

def get_mysql_data(hosttag,sql,useraccount,request):
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
    try:
        if (cmp(sql,wrong_msg)):
            log_mysql_op(useraccount,sql,dbname,hosttag,request)
        results,col = mysql_query(sql,tar_username,tar_passwd,tar_host,tar_port,tar_dbname)
    except Exception, e:
        results,col = mysql_query(wrong_msg,user,passwd,host,int(port),dbname)
    return results,col,tar_dbname

#检查输入语句
def check_mysql_query(sqltext,user):
    #根据user确定能够select 的行数
    try :
        num = User.objects.get(username=user).user_profile.select_limit
    except Exception, e:
        num = select_limit
    limit = ' limit '+str(num)

    sqltext = sqltext.strip().lower()
    sqltype = sqltext.split()[0]
    list_type = ['select','show','desc','explain']
    #flag 1位有效 0为list_type中的无效值
    flag=0
    while True:
        sqltext = sqltext.strip()
        lastletter = sqltext[len(sqltext)-1]
        if (not cmp(lastletter,';')):
            sqltext = sqltext[:-1]
        else:
            break
    #判断语句中是否已经存在limit
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
        return wrong_msg

#记录用户所有操作
def log_mysql_op(user,sqltext,dbname,dbtag,request):
    user = User.objects.get(username=user)
    #lastlogin = user.last_login+datetime.timedelta(hours=8)
    #create_time = datetime.datetime.now()+datetime.timedelta(hours=8)
    lastlogin = user.last_login
    create_time = datetime.datetime.now()
    username = user.username
    sqltype=sqltext.split()[0]
    #获取ip地址
    ipaddr = get_client_ip(request)
    log = Oper_log (user=username,sqltext=sqltext,sqltype=sqltype,login_time=lastlogin,create_time=create_time,dbname=dbname,dbtag=dbtag,ipaddr=ipaddr)
    log.save()
    return 1

def get_log_data(dbtag,optype,begin,end):
    if (optype=='all'):
        #如果结束时间小于开始时间，则以结束时间为准
        if (end >= begin):
            log = Oper_log.objects.filter(dbtag=dbtag).filter(create_time__lte=end).filter(create_time__gte=begin).order_by("-create_time")[0:100]
        else:
            log = Oper_log.objects.filter(dbtag=dbtag).filter(create_time__lte=end).order_by("-create_time")[0:100]
    else:
        if (end >=begin):
            log = Oper_log.objects.filter(dbtag=dbtag).filter(sqltype=optype).filter(create_time__lte=end).filter(create_time__gte=begin).order_by("-create_time")[0:100]
        else:
            log = Oper_log.objects.filter(dbtag=dbtag).filter(sqltype=optype).filter(create_time__lte=end).order_by("-create_time")[0:100]
    return log


def check_explain (sqltext):
    sqltext = sqltext.strip().lower()
    sqltype = sqltext.split()[0]
    if (sqltype =='select'):
        sqltext = 'explain extended '+sqltext
        return sqltext
    else:
        return wrong_msg


def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip

def main():
    return 1
if __name__=='__main__':
    main()