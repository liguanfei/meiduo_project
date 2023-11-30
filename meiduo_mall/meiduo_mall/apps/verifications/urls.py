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

app_name = "verifications"

urlpatterns = [
    # 图形验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
]
