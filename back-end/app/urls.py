from django.urls import path
from . import views

urlpatterns = [
    # 登录相关
    path("login/register/", views.RegisterView.as_view()),
    path("login/verify/", views.VerifyView.as_view()),
    path("login/login/", views.LoginView.as_view()),
    path("login/logout/", views.LogoutView.as_view()),
    path("login/password/", views.PasswordView.as_view()),
    # 用户相关
    path("user/info/", views.InfoView.as_view()),
    path("user/changepwd/", views.ChangePasswordView.as_view()),
    path("user/modify/", views.UpdateInfoView.as_view()),
    path("user/addmask/", views.AddMaskView.as_view()),
    path("user/deletemask/", views.DelMaskView.as_view()),
    path("user/updatemask/", views.UpdateMaskView.as_view()),
    # 搜索相关
    path("search/common/", views.CommonSearchView.as_view()),
    path("search/recommend/", views.RecommendSearchView.as_view()),
    # 标签相关
    path("tag/list/", views.ListTagView.as_view()),
]
