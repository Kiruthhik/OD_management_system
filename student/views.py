from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.db.models import Q
from .helper import *
from .models import *
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
    student = Student.objects.get(user=request.user)
    #approved_ods = student_OD.objects.filter(student = student,hod_approval=True)
    approved_ods = student_OD.objects.filter(
        Q(student=student) | Q(teammates=student),
        hod_approval=True
        ).distinct()
    print(approved_ods)
    #pending_ods = student_OD.objects.filter(student = student,hod_approval=False, OD_rejection=False)
    pending_ods = student_OD.objects.filter(
        Q(student=student) | Q(teammates=student),
        hod_approval=False,OD_rejection=False
        ).distinct()
    print(pending_ods)
    #rejected_ods = student_OD.objects.filter(student = student,OD_rejection=True)
    rejected_ods = student_OD.objects.filter(
        Q(student=student) | Q(teammates=student),
        OD_rejection=True
        ).distinct()
    print(rejected_ods)
    context ={
        'approved_ods':approved_ods,
        'pending_ods':pending_ods,
        'rejected_ods':rejected_ods
    }
    return render(request, 'student_home.html',context)

def apply_OD(request):
    if request.method == 'POST':
        create_OD(request)
        messages.success(request, 'OD request created successfully')
        return redirect('student_home')
    mentors = Faculty.objects.all()
    return render(request, 'apply_OD.html',{'mentors':mentors})

def OD_status(request,id):
    od = student_OD.objects.get(id=id)
    return render(request, 'student_OD.html',{'od':od})