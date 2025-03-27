from . import views
from django.urls import path

urls = [
    path('student_login',views.login,name='student_login'),
    path('home',views.home,name='student_home')
]