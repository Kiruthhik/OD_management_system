from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
# Create your views here.
from student.models import *

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='faculty').exists():
            auth_login(request, user)
            return redirect('faculty_home')
        else:
            messages.error(request, 'Invalid Credentials or you are not a faculty')
            #return render(request, 'faculty_login.html')
    return render(request, 'faculty_login.html')

def home(request):
    faculty = Faculty.objects.get(user=request.user)
    od_requests = student_OD.objects.filter(class_incharge=faculty, class_incharge_approval=False)
    print(od_requests)
    classes = faculty.handles.all()
    student_with_od = {}
    for cls in classes:
        #approved_students = Student.objects.filter(ODs__ClassOf=cls, ODs__hod_approval=True).distinct()
        student_with_od[cls] = list(student_OD.objects.filter(ClassOf=cls, hod_approval=True))
    context = {
        'od_requests': od_requests,
        'classes': classes,
        'student_with_od': student_with_od
    }
    print(context)
    return render(request, 'faculty_home.html', context)

def od_details(request,id):
    od = student_OD.objects.get(id=id)
    context = {
        'od': od
    }
    return render(request, 'od_details.html', context)