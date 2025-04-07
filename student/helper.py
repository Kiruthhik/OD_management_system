
from .models import *

def create_OD(request):
        event_name = request.POST['eventName']
        event_type = request.POST['eventType']
        venue = request.POST['venue']
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']
        # mentor_name = request.POST['mentor']
        # mentor_user_obj = User.objects.get(username=mentor_name)
        #mentor = Faculty.objects.get(user=mentor_user_obj)
        is_team = request.POST['isTeam']
        if is_team == 'on':
            is_team = True  
        else:
            is_team = False
        student = Student.objects.get(user=request.user)
        Classs = student.studies_in.all()[0]
        class_incharge = Classs.class_incharge
        print(event_type, venue, start_date, end_date, start_time, end_time)
        od = student_OD.objects.create(student = student,ClassOf = Classs, class_incharge = class_incharge ,eventName=event_name ,eventType=event_type, venue=venue, start_date=start_date, end_date=end_date,isTeam=is_team)
        od.save()
        teammates = request.POST.getlist('teammates[]')
        for tm in teammates:
            tm_user_obj = User.objects.get(username=tm)
            tm_student = Student.objects.get(user=tm_user_obj)
            od.teammates.add(tm_student)
        od.save()
        print(teammates)
        return