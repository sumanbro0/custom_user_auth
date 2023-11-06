from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.signup_view,name='signup' ),
    path('login/',views.login_page,name='login' ),
    path('verify/<email_token>/',views.activate_email,name='signup' ),
]