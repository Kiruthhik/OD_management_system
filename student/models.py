from django.db import models
from django.contrib.auth.models import User
# from django.apps import apps  # ✅ Fix: Use apps.get_model to avoid circular import

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     roll_number = models.CharField(max_length=10)
#     department = models.CharField(max_length=50)
#     year = models.CharField(max_length=10)

#     def __str__(self):
#         return self.user.first_name

# class Class(models.Model):
#     section = models.CharField(max_length=10)
#     department = models.CharField(max_length=50)
#     year = models.CharField(max_length=10)
#     class_incharge = models.OneToOneField('faculty.Faculty', related_name='incharge_of', on_delete=models.CASCADE)  # ✅ Fix: Use 'faculty.Faculty' instead of direct import
#     faculties = models.ManyToManyField('faculty.Faculty', related_name='handles')  # ✅ Fix: Use string reference
#     students = models.ManyToManyField(Student, related_name='studies_in')

#     def __str__(self):
#         return f"{self.department} {self.year} {self.section}"

# class student_OD(models.Model):  # ✅ Fix: Typo in Model
#     students = models.ManyToManyField(Student, related_name='ODs')
#     eventName = models.CharField(max_length=50)
#     eventType = models.CharField(max_length=50)
#     venue = models.CharField(max_length=50)
#     proof = models.FileField(upload_to='proofs/', blank=True, null=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     isTeam = models.BooleanField(default=False)
#     mentor = models.ForeignKey('faculty.Faculty', related_name='mentors', blank=True, null=True, on_delete=models.SET_NULL)  # ✅ Fix: Use 'faculty.Faculty'
#     mentor_approval = models.BooleanField(default=False)
#     class_incharge = models.ForeignKey('faculty.Faculty', related_name='OD_to_be_approve', on_delete=models.CASCADE)  # ✅ Fix: Use string reference
#     class_incharge_approval = models.BooleanField(default=False)
#     OD_rejection = models.BooleanField(default=False)
#     academic_head_approval = models.BooleanField(default=False)
#     hod_approval = models.BooleanField(default=False)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10)

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    faculty_type = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name

class Class(models.Model):
    section = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    students = models.ManyToManyField(Student, related_name='studies_in')
    faculties = models.ManyToManyField(Faculty, related_name='handles')
    class_incharge = models.OneToOneField(Faculty, related_name='incharge_of', on_delete=models.CASCADE)

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
    mentor = models.ForeignKey(Faculty, related_name='mentors', blank=True, null=True, on_delete=models.SET_NULL)
    mentor_approval = models.BooleanField(default=False)
    class_incharge = models.ForeignKey(Faculty, related_name='OD_to_be_approve', on_delete=models.CASCADE)
    class_incharge_approval = models.BooleanField(default=False)
    OD_rejection = models.BooleanField(default=False)
    academic_head_approval = models.BooleanField(default=False)
    hod_approval = models.BooleanField(default=False)

    def __str__(self):
        return self.eventName + " " + self.start_date.strftime('%Y-%m-%d') + " " + self.end_date.strftime('%Y-%m-%d')
    
class faculty_OD(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='ODs', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.faculty.user.username +"applies for "+ self.description