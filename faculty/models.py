# from django.db import models
# from django.contrib.auth.models import User
# from django.apps import apps  # ✅ Fix: Use apps.get_model to avoid circular import

# class Faculty(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField(max_length=50)
#     faculty_type = models.CharField(max_length=20, choices=[('HOD', 'HOD'), ('teacher', 'Teacher'), ('Academic Head', 'Academic Head'), ('DC', 'DC')])  # ✅ Fix: Use CharField with choices
#     handles = models.ManyToManyField('student.Class', related_name='faculties')  # ✅ Fix: Use string reference

#     def __str__(self):
#         return self.user.first_name

# class faculty_OD(models.Model):
#     faculty = models.ForeignKey(Faculty, related_name='ODs', on_delete=models.CASCADE)
#     description = models.CharField(max_length=100)

# from django.db import models
# from django.contrib.auth.models import User

# class Faculty(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField(max_length=50)
#     faculty_type = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.user.first_name
