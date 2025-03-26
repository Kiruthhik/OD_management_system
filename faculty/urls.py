from django.urls import path
from . import views
url_patterns = [
    path('login',views.login,name='faculty_login'),
]