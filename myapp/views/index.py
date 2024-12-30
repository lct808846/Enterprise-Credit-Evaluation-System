from django import template

from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from myadmin.models import EnterpriseAll,Profile
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


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
#         load_template = request.path.split('/')[-1]
#         context['segment'] = load_template
#         html_template = loader.get_template('myapp/' + load_template)
#         return HttpResponse(html_template.render(context, request))
#
#     except template.TemplateDoesNotExist:
#
#         html_template = loader.get_template('myapp/404.html')
#         return HttpResponse(html_template.render(context, request))
#
#     except:
#         html_template = loader.get_template('myapp/500.html')
#         return HttpResponse(html_template.render(context, request))

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

@login_required(login_url="/login/")
def table_view(request):
    context = {}
    kw = request.GET.get('keyword', '')
    # 如果有关键词，则根据关键词过滤公司列表
    if kw:
        companies = EnterpriseAll.objects.filter(firm_name__contains=kw)
    else:
        companies = EnterpriseAll.objects.all()

    items_per_page = 25
    paginator = Paginator(companies, items_per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['companies'] = page_obj
    context['is_paginated'] = True if paginator.num_pages > 1 else False
    context['paginator'] = paginator
    context['keyword'] = kw
    context['segment'] = 'tables'
    # 如果是 AJAX 请求，则返回 JSON 数据
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for company in page_obj.object_list:
            data.append({
                'id': company.id,
                'firm_name': company.firm_name,
                'est_date': company.est_date,
                'legal_rep': company.legal_rep,
                'ope_scope': company.ope_scope,
            })
        return JsonResponse({
            'data': data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'num_pages': paginator.num_pages,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        })

    return render(request, 'myapp/tables.html', context)

@login_required(login_url="/login/")
def company_detail(request, id):
    companies = EnterpriseAll.objects.get(id=id)
    context = {
        'company': companies,
    }
    return render(request, 'myapp/company_detail.html', context)

@login_required(login_url="/login/")
def profile(request):
    context = {}
    context['segment'] = 'profile'
    return render(request, 'myapp/profile.html', context)

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            # Save the uploaded file to the user's profile
            user_profile = Profile.objects.get_or_create(user=request.user)[0]
            if user_profile.profile_picture:
                default_storage.delete(user_profile.profile_picture.path)  # 删除旧的头像文件
            user_profile.profile_picture = profile_pic
            user_profile.save()
    return redirect('profile')