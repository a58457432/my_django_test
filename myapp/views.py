import sys,json,os,datetime
from django.template.context import RequestContext
from django.shortcuts import render,render_to_response
from django.contrib import auth
from form import AddForm,LoginForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

path='./myapp/include'
sys.path.insert(0,path)
import function as func
# Create your views here.
@login_required
def index(request):
    return render(request, 'include/base.html')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render(request,'include/base.html')
            else:
                return render_to_response('login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
        else:
            return render_to_response('login.html', RequestContext(request, {'form': form,}))

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")
'''
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/invalid/")
'''




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

def mysql_query(request):
    if request.user.is_authenticated():
        obj_list = func.get_mysql_hostlist()
        print type(obj_list)
        if request.method == 'POST':
            form = AddForm(request.POST)
            if form.is_valid():
                a = form.cleaned_data['a']
                c = request.POST['cx']
                (data_mysql,collist) = func.get_mysql_data(c,a)
                return render(request,'mysql_query.html',{'form': form,'objlist':obj_list,'book_list':data_mysql,'col':collist})
        else:
            form = AddForm()
            return render(request, 'mysql_query.html', {'form': form,'objlist':obj_list})
    else:
        return HttpResponseRedirect("/accounts/login/")


