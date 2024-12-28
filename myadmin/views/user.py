from lib2to3.fixes.fix_input import context
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import random

from django.contrib.auth.models import User



def index(request,pIndex=1):
    '''浏览信息'''
    mywhere=[]
    list = User.objects.all()

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询用户账号或邮箱中只要含有关键字的都可以
        list = list.filter(Q(username__contains=kw) | Q(email__contains=kw))
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        list = list.filter(is_active=status)
        mywhere.append("status="+status)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #list2 = User.objects.all() #获取所有信息
    #封装信息加载模板输出
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/index.html",context)

def add(request):
    '''加载添加页面'''
    return render(request,"myadmin/user/add.html")

def insert(request):
    '''执行添加'''
    try:
        # 检查用户名是否已存在
        if User.objects.filter(username=request.POST['username']).exists():
            context = {"info": "该用户已存在！"}
            return render(request,"myadmin/info.html",context)  # 用户名已存在提示
        ob = User()
        ob.username = request.POST['username']
        ob.email = request.POST['email']
        #获取密码
        s = request.POST['password']
        r = request.POST['repassword']
        if s == r:
            ob.set_password(s)
            ob.is_staff = 0
            ob.is_superuser = 0
            ob.date_joined = datetime.now()
            ob.save()
            context={"info":"添加成功！"}
        else:
            raise NameError
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid):
    '''删除信息'''
    try:
        ob = User.objects.get(id=uid)
        if ob.id != request.session['adminuser']['id']:
            # ob.is_active = 9
            ob.delete()
            context={"info":"删除成功！"}
        else:
            context={"info":"删除失败"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}

    return JsonResponse(context)
    #return render(request,"myadmin/info.html",context)


def edit(request,uid):
    '''加载编辑信息页面'''
    try:
        ob = User.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,uid):
    '''执行编辑信息'''
    try:
        ob = User.objects.get(id=uid)
        ob.email = request.POST['email']
        ob.is_superuser = request.POST['is_superuser']
        ob.is_active = request.POST['is_active']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)


def resetpass(request,uid):
    '''加载重置会员密码信息页面'''
    try:
        ob = User.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/user/resetpass.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def doresetpass(request,uid):
    '''执行编辑信息'''
    try:
        ob = User.objects.get(id=uid)
        s = request.POST['password']
        ob.set_password(s)
        ob.save()
        context={"info":"密码重置成功！"}
    except Exception as err:
        print(err)
        context={"info":"密码重置失败"}
    return render(request,"myadmin/info.html",context)
