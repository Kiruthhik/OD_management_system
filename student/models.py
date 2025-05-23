from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10)
    department = models.CharField(max_length=50,default="CSE")
    section = models.CharField(max_length=10,default="A")
    year = models.IntegerField(default="2")
    def __str__(self):
        return self.user.username + " " + self.user.first_name + " " + self.user.last_name

class Faculty(models.Model):
    class FacultyType(models.TextChoices):
        HOD = "HOD", "HOD"
        TEACHING = "Teaching", "Teaching"
        ACADEMIC_HEAD_1 = "Academic Head 1st Year", "Academic Head 1st Year"
        ACADEMIC_HEAD_2 = "Academic Head 2nd Year", "Academic Head 2nd Year"
        ACADEMIC_HEAD_3 = "Academic Head 3rd Year", "Academic Head 3rd Year"
        DC = "DC", "DC"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    faculty_code = models.CharField(max_length=15,unique=True)
    faculty_type = models.CharField(
        max_length=50,
        choices=FacultyType.choices,
        default=FacultyType.TEACHING
    )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Class(models.Model):
    section = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    students = models.ManyToManyField(Student, related_name='studies_in')
    faculties = models.ManyToManyField(Faculty, related_name='handles')
    class_incharge = models.OneToOneField(Faculty,null=True, related_name='incharge_of', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} {self.year} {self.section}"

class student_OD(models.Model):
    student = models.ForeignKey(Student, related_name='ODs', on_delete=models.CASCADE)
    ClassOf = models.ForeignKey(Class, related_name='ODs', on_delete=models.CASCADE)
    eventName = models.CharField(max_length=50)
    eventType = models.CharField(max_length=50)
    venue = models.CharField(max_length=50)
    proof = models.FileField(upload_to='proofs/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    isTeam = models.BooleanField(default=False)
    teammates = models.ManyToManyField(Student, related_name='teammates', blank=True)
    class_incharge = models.ForeignKey(Faculty, related_name='OD_to_be_approve', on_delete=models.CASCADE)
    class_incharge_approval = models.BooleanField(default=False)
    OD_rejection = models.BooleanField(default=False)
    academic_head_approval = models.BooleanField(default=False)
    hod_approval = models.BooleanField(default=False)

    def __str__(self):
        return self.eventName + " " + self.eventType + " " + self.start_date.strftime('%Y-%m-%d') + " " + self.end_date.strftime('%Y-%m-%d')
    
class faculty_OD(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='ODs', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.faculty.user.username +"applies for "+ self.description