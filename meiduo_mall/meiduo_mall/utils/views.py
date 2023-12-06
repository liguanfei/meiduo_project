#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project    : meiduo_project
@File       : views.py
@IDE        : PyCharm
@Author     : liguanfei
@Date       : 2023/12/6 17:11
@Function   : 
"""
from django.contrib.auth.decorators import login_required


# 添加扩展类:
# 因为这类扩展其实就是 Mixin 扩展类的扩展方式
# 所以我们起名时, 最好也加上 Mixin 字样, 不加也可以.
class LoginRequiredMixin(object):
    """验证用户是否登录的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的 as_view() 函数
        view = super().as_view()
        return login_required(view)
