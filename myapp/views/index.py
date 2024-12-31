from django import template
from django.contrib import messages

from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.urls import reverse

from myadmin.models import EnterpriseAll, Profile, Favorite,ScoreWeight
from ..forms import LoginForm, SignUpForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import loader
from ..calculate import calculate_company_score

# Create your views here.



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('myapp/index.html')
    return HttpResponse(html_template.render(context, request))

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

    items_per_page = 30
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
def score(request, id):
    company = EnterpriseAll.objects.get(id=id)
    company.score = calculate_company_score(company)
    context = {
        'company': company,
        'score': company.score,
    }
    return render(request, 'myapp/score.html', context)

@login_required(login_url="/login/")
def profile(request):
    context = {}
    context['segment'] = 'profile'
    return render(request, 'myapp/profile.html', context)

@login_required(login_url="/login/")
def map(request):
    context = {}
    context['segment'] = 'map'
    kw = request.GET.get('keyword', '')
    context['keyword'] = kw
    return render(request, 'myapp/map.html', context)

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def query(request):
    context = {}
    kw = request.GET.get('keyword', '')

    # 如果有关键词，则根据关键词过滤公司列表
    if kw:
        companies = EnterpriseAll.objects.filter(firm_name__contains=kw)
    else:
        companies = EnterpriseAll.objects.all()

    items_per_page = 30
    paginator = Paginator(companies, items_per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 获取当前用户的收藏列表
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('company_id', flat=True))

    # 为每家公司计算评分
    for company in page_obj.object_list:
        company.score = calculate_company_score(company)

    context['companies'] = page_obj
    context['is_paginated'] = True if paginator.num_pages > 1 else False
    context['paginator'] = paginator
    context['keyword'] = kw
    context['segment'] = 'query'
    context['user_favorites'] = user_favorites

    # 如果是 AJAX 请求，则返回 JSON 数据
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for company in page_obj.object_list:
            data.append({
                'id': company.id,
                'firm_name': company.firm_name,
                'score': company.score,  # 包含评分
                'favorited': company.id in user_favorites,  # 包含收藏状态
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

    return render(request, 'myapp/query.html', context)

@login_required(login_url="/login/")
def toggle_favorite(request):
    if request.method == 'POST':
        company_id = request.POST.get('id')
        company = EnterpriseAll.objects.get(id=company_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, company=company)
        if not created:
            # 如果收藏已经存在，则删除它
            favorite.delete()
            return JsonResponse({'success': True, 'favorited': False})
        else:
            # 如果收藏是新创建的，则返回成功信息
            return JsonResponse({'success': True, 'favorited': True})

    return JsonResponse({'success': False}, status=400)


@login_required(login_url="/login/")
def favorites(request):
    # 获取当前登录用户收藏的所有公司
    favorite_companies = EnterpriseAll.objects.filter(favorite__user=request.user)
    context = {}
    kw = request.GET.get('keyword', '')

    # 如果有关键词，则根据关键词过滤公司列表
    if kw:
        companies = favorite_companies.filter(firm_name__contains=kw)
    else:
        companies = favorite_companies

    items_per_page = 5
    paginator = Paginator(companies, items_per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 获取当前用户的收藏列表
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('company_id', flat=True))

    # 为每家公司计算评分
    for company in page_obj.object_list:
        company.score = calculate_company_score(company)

    context['companies'] = page_obj
    context['is_paginated'] = True if paginator.num_pages > 1 else False
    context['paginator'] = paginator
    context['keyword'] = kw
    context['segment'] = 'query'
    context['user_favorites'] = user_favorites
    context['segment'] = 'favorites'
    # 如果是 AJAX 请求，则返回 JSON 数据
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for company in page_obj.object_list:
            data.append({
                'id': company.id,
                'firm_name': company.firm_name,
                'score': company.score,  # 包含评分
                'favorited': company.id in user_favorites,  # 包含收藏状态
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
    return render(request, 'myapp/favorites.html', context)

@login_required(login_url="/login/")
def settings(request):
    return render(request, 'myapp/settings.html', {'segment': 'settings'})


@login_required(login_url="/login/")
def update_weights(request):
    if request.method == 'POST':
        try:
            execute_weight = float(request.POST.get('execute_weight'))
            case_weight = float(request.POST.get('case_weight'))
            money_weight = float(request.POST.get('money_weight'))
            judge_weight = float(request.POST.get('judge_weight'))

            total_weight = execute_weight + case_weight + money_weight + judge_weight
            if abs(total_weight - 1) > 1e-6:  # 检查权重之和是否接近1
                messages.error(request, "权重之和必须为1，请重新输入。")
                return redirect(reverse('settings'))

            weights, created = ScoreWeight.objects.get_or_create(pk=1)
            weights.execute_weight = execute_weight
            weights.case_weight = case_weight
            weights.money_weight = money_weight
            weights.judge_weight = judge_weight
            weights.save()

            messages.success(request, "权重已成功更新。")
        except Exception as e:
            messages.error(request, f"更新权重时出错: {str(e)}")

    return redirect(reverse('settings'))