import random
from datetime import datetime


from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from myadmin.models import User,Astock
from django.shortcuts import render



# Create your views here.

def index(request):
    return redirect(reverse('web_index_default'))

def webIndex(request,pIndex=1):
    kw = request.GET.get("keyword", "")
    mywhere = ''

    if kw:
        list1 = Astock.objects.filter(company__contains=kw)
        mywhere = '?keyword=%s' % kw
    else:
        list1 = Astock.objects.all()

    p = Paginator(list1, 15)  # 每页显示15条记录

    if pIndex <= 0:
        pIndex = 1
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    pIndex = int(pIndex)
    list = p.page(pIndex)
    plist = p.page_range

    return render(request, 'myapp/index.html',
                  {'list': list, 'plist': plist, 'pIndex': pIndex, 'keyword': kw, 'mywhere': mywhere})

def login(request):
    '''加载登录页面'''
    return render(request,"myapp/login.html")

def dologin(request):
    '''执行登录'''

    #验证判断
    verifycode = request.session['verifycode'].lower()
    code = request.POST['code'].lower()
    if verifycode != code:
        #验证码错误！
        return redirect(reverse('web_login')+"?typeinfo=2")

    try:
        #根据登录账号获取用户信息
        user = User.objects.get(username=request.POST['username'])
        # 校验当前用户状态是否是管理员
        if user.status == 6 or user.status==1:
            #获取密码并md5
            import hashlib
            md5 = hashlib.md5()
            n = user.password_salt
            s = request.POST['pass']+str(n)
            md5.update(s.encode('utf-8'))
            # 校验密码是否正确
            if user.password_hash == md5.hexdigest():
                # 将当前登录成功用户信息以adminuser这个key放入到session中
                request.session['webuser']=user.toDict()
                return redirect(reverse('web_index_default'))
            else:
                # 登录密码错误
                return redirect(reverse('web_login')+"?typeinfo=5")
        else:
            # 此用户非管理账号
            return redirect(reverse('web_login')+"?typeinfo=4")
    except Exception as err:
        print(err)
        # 登录账号不存在！
        return redirect(reverse('web_login')+"?typeinfo=3")

def register(request):
    '''加载注册页面'''
    return render(request,"myapp/register.html")

def doregister(request):
    '''执行注册'''
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        # 获取密码并md5
        import hashlib
        md5 = hashlib.md5()
        rmd5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        r = request.POST['repassword'] + str(n)
        md5.update(s.encode('utf-8'))
        rmd5.update(r.encode('utf-8'))
        if md5.hexdigest() == rmd5.hexdigest():
            ob.password_hash = md5.hexdigest()
            ob.password_salt = n
            ob.status = 1
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            return redirect(reverse('web_login')+"?typeinfo=1")
        else:
            raise NameError
    except Exception as err:
        print(err)
        return redirect(reverse('web_register')+"?typeinfo=1")

def logout(request):
    '''执行退出'''
    del request.session['webuser']
    request.session['cartlist'] = {}
    return redirect(reverse('web_login'))

def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
