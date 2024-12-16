from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
import time

from myadmin.models import Shop

def index(request,pIndex=1):
    '''浏览信息'''
    smod = Shop.objects
    mywhere=[]
    list = smod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(name__contains=kw)
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        list = list.filter(status=status)
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

    #封装信息加载模板输出
    context = {"shoplist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/shop/index.html",context)

def add(request):
    '''加载添加页面'''
    return render(request,"myadmin/shop/add.html")

def insert(request):
    '''执行添加'''
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+cover_pic,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic",None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+banner_pic,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        #实例化model，封装信息，并执行添加
        ob = Shop()
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.address = request.POST['address']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
    return render(request,"myadmin/info.html",context)

def delete(request,sid):
    '''删除信息'''
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    #return render(request,"myadmin/info.html",context)
    return JsonResponse(context)


def edit(request,sid):
    '''加载编辑信息页面'''
    try:
        ob = Shop.objects.get(id=sid)
        context={"shop":ob}
        return render(request,"myadmin/Shop/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,sid):
    '''执行编辑信息'''
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.address = request.POST['address']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)