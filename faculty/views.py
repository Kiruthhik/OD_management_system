from django.shortcuts import render
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='faculty').exists():
            auth_login(request, user)
            return render(request, 'faculty_home.html')
        else:
            messages.error(request, 'Invalid Credentials or you are not a faculty')
            #return render(request, 'faculty_login.html')
    return render(request, 'faculty_login.html')