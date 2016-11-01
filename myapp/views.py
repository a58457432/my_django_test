import sys,json,os,datetime
from django.template.context import RequestContext
from django.shortcuts import render,render_to_response
from django.contrib import auth
from form import AddForm,LoginForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
path='./myapp/include'
sys.path.insert(0,path)
import function as func
# Create your views here.
'''
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
'''

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def mytest(request):
    results,col = func.mysql_query('select host from db_servers_mysql;')
    obj_list=[]
    for row in results:
        obj_list.append(row[0])
    print type(obj_list)

    if request.method == 'POST' or request.method=='GET':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            (booklist,collist) = func.mysql_query(a)
            return render(request,'index.html',{'form': form,'objlist':obj_list,'book_list':booklist,'col':collist})
    else:
        form = AddForm()
        return render(request, 'index.html', {'form': form,'objlist':obj_list})

@login_required(login_url='/accounts/login/')
@permission_required('myapp.can_mysql_query', login_url='/')
def mysql_query(request):
    #print request.user.username
    print request.user.has_perm('myapp.can_mysql_query')
    print "what the fuck"
    obj_list = func.get_mysql_hostlist(request.user.username)
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            c = request.POST['cx']
            try:
                if request.POST['explain']== u'1':
                    explaintag = request.POST['explain']
                    a = func.check_explain (a)
            except Exception,e:
                a = func.check_mysql_query(a,request.user.username)
            print a
            (data_mysql,collist,dbname) = func.get_mysql_data(c,a,request.user.username)
            #print request.POST

            return render(request,'mysql_query.html',{'form': form,'objlist':obj_list,'data_list':data_mysql,'col':collist,'choosed_host':c,'dbname':dbname})
        else:
            return render(request, 'mysql_query.html', {'form': form,'objlist':obj_list})
    else:
        form = AddForm()
        return render(request, 'mysql_query.html', {'form': form,'objlist':obj_list})


