#后台管理子路由文件
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.views.static import serve

from djangoProject import settings
from myapp.views import index

urlpatterns = [
    # 首页
    path('', index.index, name='index'),
    path('login/', index.Login, name="web_login"),
    path('register/', index.Register, name="web_register"),
    path("logout/", LogoutView.as_view(next_page='/login'), name="web_logout"),
    path('tables/', index.table_view, name='tables'),
    path('company/<str:id>/', index.company_detail, name='company_detail'),
    path('profile/', index.profile, name='profile'),
    path('update_profile_pic/', index.update_profile_pic, name='update_profile_pic'),
    path('query', index.query, name='query'),
    path('favorites', index.favorites, name='favorites'),
    path('toggle_favorite',index.toggle_favorite, name='toggle_favorite'),
    path('map', index.map, name='map'),
    path('settings', index.settings, name='settings'),
]
