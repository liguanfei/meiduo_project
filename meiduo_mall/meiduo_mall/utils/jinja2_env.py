#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project    : meiduo_project
@File       : jinja2_env.py
@IDE        : PyCharm
@Author     : liguanfei
@Date       : 2023/11/29 14:42
@Function   : 
"""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


"""
确保可以使用Django模板引擎中的{% url('') %} {% static('') %}这类的语句 
"""
