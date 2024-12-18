#后台管理子路由文件
from django.urls import path, include
from myapp.views import index
urlpatterns = [
    # 首页
    path('', index.index, name='index'),
    path('login', index.login, name="web_login"),
    path('dologin', index.dologin, name="web_dologin"),
    path('register', index.register, name="web_register"),
    path('doregister', index.doregister, name="web_doregister"),
    path('logout', index.logout, name="web_logout"),
    path('verify', index.verify, name="web_verify"), #验证码

    #为url路由添加请求前缀web/,凡是带此前缀的url地址必须登录后才可访问
    path('web/',include([
        path('<int:pIndex>/', index.webIndex, name="web_index"),
        path('', index.webIndex, {'pIndex': 1}, name='web_index_default'),  # 设置默认 pIndex 为 1
    ]))
]
