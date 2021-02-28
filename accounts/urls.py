from knox.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('user', UserAPIView.as_view()),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    # path('adminlogin', AdminLoginAPIView.as_view()),
    path('logout', LogoutView.as_view(), name='knox_logout')
]