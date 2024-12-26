# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：     urls.py
   Description :
   Author :         FHQI
   date ：          2021-08-19
-------------------------------------------------
"""
from django.conf.urls import url

from backend.views import authenticate_user, get_products, register_user

urlpatterns = [
    url("authenticate_user", authenticate_user, ),
    url("get_products", get_products, ),
    url("register_user", register_user, ),
]

