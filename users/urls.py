# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('healthz/', views.health_check, name='health_check'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

