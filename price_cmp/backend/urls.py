# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：     urls.py
   Description :
   Author :         FHQI
   date ：          2021-08-19
-------------------------------------------------
"""
from django.urls import path

from backend.views import (authenticate_user, get_products,
                           register_user, add_reminder,
                           delete_reminder, detail_info,
                           get_reminder, send_verification_code, verify_verification_code)

urlpatterns = [
    path("authenticate_user", authenticate_user, ),
    path("get_products", get_products, ),
    path("register_user", register_user, ),
    path("add_reminder", add_reminder, ),
    path("delete_reminder", delete_reminder, ),
    path("detail_info", detail_info, ),
    path("get_reminder", get_reminder, ),
    path("send_code", send_verification_code, ),
    path("verify_code", verify_verification_code, ),
]
