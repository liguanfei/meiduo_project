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

app_name = "contents"

urlpatterns = [
    # 首页广告
    url(r'^$', views.IndexView.as_view(), name='index'),
]
