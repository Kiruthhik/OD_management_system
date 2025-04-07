from student.models import *

def OD_requests(faculty):
    od_requests = []
    if(faculty.faculty_type == Faculty.FacultyType.TEACHING):
        print("Teaching")
        od_requests = (student_OD.objects.filter(class_incharge=faculty, class_incharge_approval=False, OD_rejection=False))
    elif(faculty.faculty_type == Faculty.FacultyType.HOD):
        print("HOD")
        od_requests = (student_OD.objects.filter(academic_head_approval=True, hod_approval=False))
    elif(faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_1):
        print("Academic Head 1")
        od_requests = (student_OD.objects.filter(class_incharge_approval=True, academic_head_approval=False,student__year = 1))
        
    elif(faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_2):
        print("Academic Head 2")
        od_requests = (student_OD.objects.filter(class_incharge_approval=True, academic_head_approval=False,student__year = 2))
    
    elif(faculty.faculty_type == Faculty.FacultyType.ACADEMIC_HEAD_3):
        print("Academic Head 3")
        od_requests = (student_OD.objects.filter(class_incharge_approval=True, academic_head_approval=False,student__year = 3))
    return od_requests