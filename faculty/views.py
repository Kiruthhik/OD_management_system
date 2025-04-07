from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
# Create your views here.
from student.models import *
from .helper import *

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        #add the user to the student group if not already in the group 
        if user is not None and user.groups.filter(name='faculty').exists():
            auth_login(request, user)
            return redirect('faculty_home')
        else:
            messages.error(request, 'Invalid Credentials or you are not a faculty')
            #return render(request, 'faculty_login.html')
    return render(request, 'faculty_login.html')

def home(request):
    faculty = Faculty.objects.get(user=request.user)
    print(faculty.faculty_type)
    if(faculty.faculty_type == Faculty.FacultyType.HOD):
        return hod_home(request, faculty)
    od_requests = OD_requests(faculty)

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

def hod_home(request, faculty):
    od_requests = student_OD.objects.filter(academic_head_approval=True, hod_approval=False)
    all_od_requests = student_OD.objects.all()
    content = {
        'od_requests': od_requests,
        'all_od_requests': all_od_requests
    }
    print(od_requests)
    return render(request, 'hod-home.html',content)

def od_details(request,id):
    od = student_OD.objects.get(id=id)
    context = {
        'od': od
    }
    return render(request, 'od_details.html', context)

#it is used to approve or reject the od request by the class incharge or hod or academic head , ajax call is used to call this function
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
def process_od(request, od_id, action):
    od = get_object_or_404(student_OD, id=od_id)
    print(od_id,action)
    faculty = Faculty.objects.get(user=request.user)
    if action == 'approve':
        if faculty.faculty_type == Faculty.FacultyType.TEACHING:
            od.class_incharge_approval = True
            od.save()
            return JsonResponse({'success': True, 'message': 'OD Approved'})
        elif((faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_1 or faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_2 or faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_3 )):
            od.academic_head_approval = True
            od.save()
            return JsonResponse({'success': True, 'message': 'OD Approved'})
        elif faculty.faculty_type == Faculty.FacultyType.HOD:
            print("HOD approval")
            od.hod_approval = True
            od.save()
            return JsonResponse({'success': True, 'message': 'OD Approved'})
        return JsonResponse({'success': False, 'message': 'OD already approved'})

    elif action == 'reject':
        if not od.class_incharge_approval:
            od.OD_rejection = True
            od.save()
            return JsonResponse({'success': True, 'message': 'OD Rejected'})
        return JsonResponse({'success': False, 'message': 'OD already approved'})

    return JsonResponse({'success': False, 'message': 'Invalid action'})