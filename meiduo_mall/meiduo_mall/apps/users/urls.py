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
]
