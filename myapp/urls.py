#后台管理子路由文件
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from myapp.views import index
urlpatterns = [
    # 首页
    path('', index.index, name='index'),
    path('login/', index.Login, name="web_login"),
    path('register/', index.Register, name="web_register"),
    path("logout/", LogoutView.as_view(next_page='/login'), name="web_logout"),
    path('myadmin/',include('myadmin.urls')),
    re_path(r'^.*\.*', index.pages, name='pages'),
]
