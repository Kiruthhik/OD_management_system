from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

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
    approved_ods = student_OD.objects.filter(student = student,hod_approval=True)
    print(approved_ods)
    pending_ods = student_OD.objects.filter(student = student,hod_approval=False, OD_rejection=False)
    print(pending_ods)
    rejected_ods = student_OD.objects.filter(student = student,OD_rejection=True)
    print(rejected_ods)
    context ={
        'approved_ods':approved_ods,
        'pending_ods':pending_ods,
        'rejected_ods':rejected_ods
    }
    return render(request, 'student_home.html',context)

def apply_OD(request):
    if request.method == 'POST':
        event_name = request.POST['eventName']
        event_type = request.POST['eventType']
        venue = request.POST['venue']
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']
        mentor_name = request.POST['mentor']
        mentor_user_obj = User.objects.get(username=mentor_name)
        mentor = Faculty.objects.get(user=mentor_user_obj)
        student = Student.objects.get(user=request.user)
        Classs = student.studies_in.all()[0]
        class_incharge = Classs.class_incharge
        print(event_type, venue, start_date, end_date, start_time, end_time, mentor)
        od = student_OD.objects.create(student = student,ClassOf = Classs, class_incharge = class_incharge ,eventName=event_name ,eventType=event_type, venue=venue, start_date=start_date, end_date=end_date, mentor=mentor)
        od.save()
        teammates = request.POST.getlist('teammates[]')
        for tm in teammates:
            tm_user_obj = User.objects.get(username=tm)
            tm_student = Student.objects.get(user=tm_user_obj)
            classs = tm_student.studies_in.all()[0]
            classIncharge = classs.class_incharge
            OD = student_OD.objects.create(student = tm_student,ClassOf = classs,class_incharge = classIncharge, eventName = event_name,eventType=event_type, venue=venue, start_date=start_date, end_date=end_date,  mentor=mentor)
            OD.save()
        print(teammates)
        return redirect('student_home')
    mentors = Faculty.objects.all()
    return render(request, 'apply_OD.html',{'mentors':mentors})

def OD_status(request,id):
    od = student_OD.objects.get(id=id)
    return render(request, 'student_OD.html',{'od':od})