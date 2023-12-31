#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project    : meiduo_project
@File       : urls.py
@IDE        : PyCharm
@Author     : liguanfei
@Date       : 2023/11/29 18:54
@Function   : 
"""
from django.conf.urls import url
from . import views

app_name = "users"

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户名登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 子路由
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
]
