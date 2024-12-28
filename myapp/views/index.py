from django import template

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from myadmin.models import Astock
from ..forms import LoginForm, SignUpForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import loader
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('myapp/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        if load_template == 'tables.html':
            kw = request.GET.get('keyword', '')
            mywhere = ''
            companies = Astock.objects.all()
            if kw:
                companies = Astock.objects.filter(company__contains=kw)
                mywhere = '?keyword=%s' % kw
            # 设置每页显示的条目数量
            items_per_page = 10

            # 创建分页器对象
            paginator = Paginator(companies, items_per_page)

            # 从请求中获取当前页面编号，默认为第一页
            page_number = request.GET.get('page', 1)

            try:
                # 获取指定页面的对象
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                # 如果页面不是整数，则递送第一页。
                page_obj = paginator.page(1)
            except EmptyPage:
                # 如果页面超出范围（例如9999），则递送最后一页。
                page_obj = paginator.page(paginator.num_pages)
            context['companies'] =page_obj
            context['is_paginated'] = True if paginator.num_pages > 1 else False
            context['paginator'] = paginator
            context['keyword'] = kw
            context['mywhere'] = mywhere
        html_template = loader.get_template('myapp/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('myapp/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('myapp/page-500.html')
        return HttpResponse(html_template.render(context, request))
# def index(request):
#     return redirect(reverse('web_index_default'))
#
# def webIndex(request,pIndex=1):
#     kw = request.GET.get("keyword", "")
#     mywhere = ''
#
#     if kw:
#         list1 = Astock.objects.filter(company__contains=kw)
#         mywhere = '?keyword=%s' % kw
#     else:
#         list1 = Astock.objects.all()
#
#     p = Paginator(list1, 15)  # 每页显示15条记录
#
#     if pIndex <= 0:
#         pIndex = 1
#     if pIndex > p.num_pages:
#         pIndex = p.num_pages
#     pIndex = int(pIndex)
#     list = p.page(pIndex)
#     plist = p.page_range
#
#     return render(request, 'myapp/index2.html',
#                   {'list': list, 'plist': plist, 'pIndex': pIndex, 'keyword': kw, 'mywhere': mywhere})

def Login(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = '凭据无效'
        else:
            msg = '验证表单时出错'

    return render(request, "myapp/login.html", {"form": form, "msg": msg})

def Register(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = '账户创建成功 - 前往 <a href="/login">登录</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = '表单无效'
    else:
        form = SignUpForm()

    return render(request, "myapp/register.html", {"form": form, "msg": msg, "success": success})
