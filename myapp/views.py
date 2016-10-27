import sys
import json
import os
from django.shortcuts import render
from form import AddForm
from django.http import HttpResponse
import datetime
from django import forms
from django.http import JsonResponse
path='./myapp/include'
sys.path.insert(0,path)
import function as func
# Create your views here.
class Testform(forms.Form):
	user = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30)

class Person(object):
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
def sayHello(request):
    s = 'Hello World!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s </h1><p> %s </p></body></html>' % (s, current_time)
    return render(request , 'temp.html')
    #return HttpResponse(html)

def add(request):
    f = Testform()
    return render(request , 'base.html')

def index(request):
    user=Person('Max',33,'male')
    booklist=[]
    (booklist,collist) = func.mysql_query('select * from db_servers_mysql')
    i=0
    return render(request, 'home.html',{'user':user,'title':'mytitle','book_list':booklist,'col':collist})


def mytest(request):
    results,col = func.mysql_query('select host from db_servers_mysql;')
    obj_list=[]
    for row in results:
        obj_list.append(row[0])
    print type(obj_list)

    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            (booklist,collist) = func.mysql_query(a)
            return render(request,'index.html',{'form': form,'objlist':obj_list,'book_list':booklist,'col':collist})
    else:
        form = AddForm()
        return render(request, 'index.html', {'form': form,'objlist':obj_list})

def myjs(request):
    results,col = func.mysql_query('select host from db_servers_mysql;')
    obj_list=[]
    for row in results:
        obj_list.append(row[0])
    print type(obj_list)
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            (booklist,collist) = func.mysql_query(a)
            return render(request,'js.html',{'form': form,'objlist':obj_list,'book_list':booklist,'col':collist})
    else:
        form = AddForm()
        return render(request, 'js.html', {'form': form,'objlist':obj_list})
