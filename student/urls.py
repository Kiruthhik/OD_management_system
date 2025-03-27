from . import views
from django.urls import path

urls = [
    path('student-login',views.login,name='student_login'),
    path('home',views.home,name='student_home'),
    path('OD-application',views.apply_OD,name='apply_od'),
]