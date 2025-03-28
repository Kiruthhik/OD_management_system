from django.urls import path
from . import views
url_patterns = [
    path('login',views.login,name='faculty_login'),
    path('home',views.home,name='faculty_home'),
    path('od-details/<int:id>',views.od_details,name='od_details'),
]