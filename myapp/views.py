from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime
from django import forms
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
    return render(request , 'template.html',{'form':f})


'''
def index(request):
    t=loader.get_template('home.html')
    c=Context({})
    return HttpResponse(t.render(c))
    #return render(request, 'home.html')
'''
def index(request):
    user=Person('Max',33,'male')
    booklist=['python','java']
    return render(request, 'home.html',{'user':user,'title':'mytitle','book_list':booklist})