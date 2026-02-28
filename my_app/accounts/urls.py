from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("invite/", views.invite_view, name="invite"),
    path("me/", views.me_view, name="me"),
    path("me/edit/", views.ProfileUpdateView.as_view(), name="account_edit"),
    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
]