"""
User url configuration.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("login/", view=views.UserLoginView.as_view(), name="user-login"),
    path("status/", views.CheckUserStatusView.as_view(), name="user-status"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("remove/", views.UserRemoveView.as_view(), name="user-remove"),
    path("deposit/", views.UserDepositView.as_view(), name="user-deposit"),
    path("reset/", views.UserResetView.as_view(), name="user-reset"),
]
