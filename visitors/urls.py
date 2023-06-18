from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage_url'),
    path('booking/', booking, name='booking_url'),
    path('visitors/login/', LoginView.as_view(template_name='visitors_login.html'), name='login'),
    path('visitors/logout/', LogoutView.as_view(), name='logout'),
    path('visitors/signup/', SignupView.as_view(), name='signup'),
    path('booking_approve/', booking_approve, name='booking_approve')
]

