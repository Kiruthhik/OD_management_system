import os
import openpyxl
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student.models import *

class Command(BaseCommand):
    help = "Import class and faculty data from an Excel file"


    def handle(self, *args, **options):
        file_path = r"C:\Users\HP\Documents\OD management system\CSE-STAFF-LIST.xlsx"
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found!"))
            return

        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):  # Skip header
            faculty_code = str(row[0]).strip()
            section = str(row[2]).strip()
            year = int(row[3])  # If it's a float like 2.0

            if not faculty_code or not section or not year:
                print("skipped row",row)  # Print skipped row for debugging
                continue  # Skip empty rows

            print(faculty_code,section,year)  # Print faculty code for debugging
            classs = Class.objects.get_or_create(
                section=section,
                department="CSE",
                year=year,
            )
            try:
                user = User.objects.get(username=faculty_code)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with username {faculty_code} not found!"))
                continue

            try:
                faculty = Faculty.objects.get(user=user)
            except Faculty.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Faculty with username {faculty_code} not found!"))
                continue

            
            
            classs[0].faculties.add(faculty)
            

            self.stdout.write(self.style.SUCCESS(f"Added/Updated: {faculty_code} to class {section} {year}"))

        self.stdout.write(self.style.SUCCESS("Faculty import completed successfully!"))
