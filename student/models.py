from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name