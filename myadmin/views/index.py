from django.contrib.auth.hashers import check_password
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

def toDict(self):
    return {'id': self.id, 'password': self.password, 'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            'is_superuser': self.is_superuser, 'username': self.username, 'first_name': self.first_name,
            'last_name': self.last_name, 'email': self.email,
            'is_staff': self.is_staff, 'is_active': self.is_active, 'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S')}


def index(request):
    user_count = User.objects.count()  # 获取用户总数
    context = {
        'user_count': user_count,
    }
    return render(request,'myadmin/index/index.html', context)


def login(request):
    '''加载登录页面'''
    return render(request,"myadmin/index/login.html")

# 会员执行登录
def dologin(request):
    '''执行登录'''
    #验证判断
    verifycode = request.session['verifycode'].lower()
    code = request.POST['code'].lower()
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"myadmin/index/login.html",context)

    try:
        #根据登录账号获取用户信息
        user = User.objects.get(username=request.POST['username'])
        # 校验当前用户状态是否是管理员
        if user.is_superuser == 1:
            #获取密码
            s = request.POST['password']
            # 校验密码是否正确
            is_password_correct = check_password(s, user.password)
            if is_password_correct == 1:
                # 将当前登录成功用户信息以adminuser这个key放入到session中
                request.session['adminuser']=toDict(user)
                return redirect(reverse('myadmin_index'))
            else:
                context={"info":"登录密码错误！"}
        else:
            context={"info":"此用户非后台管理账号！"}
    except Exception as err:
        print(err)
        context={"info":"登录账号不存在！"}
    return render(request,"myadmin/index/login.html",context)


def logout(request):
    '''执行退出'''
    request.session.pop('adminuser', None)
    return redirect(reverse('myadmin_login'))


def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
       20, 100),100)
    # bgcolor = (242,164,247)
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