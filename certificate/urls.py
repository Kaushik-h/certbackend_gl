from django.urls import path
from .views import *

urlpatterns = [
    path('certificates', CertificateView.as_view()),
    path('allusers', AllUsersView.as_view()),
    path('alluserscertificates', AllUsersCertificateView.as_view()),
    path('sendmail', AdminSendMailView.as_view()),
]