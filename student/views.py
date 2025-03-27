from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.groups.filter(name='student').exists():
            auth_login(request, user)
            print(user)
            return redirect('student_home')

        else:
            messages.error(request, 'Invalid Credentials or you are not a student')
            return render(request, 'student_login.html')
    return render(request, 'student_login.html')

def home(request):
    return render(request, 'student_home.html')