import os
import openpyxl
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student.models import Faculty

class Command(BaseCommand):
    help = "Import faculty data from an Excel file"

    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', type=str, help="Path to the Excel file")

    def handle(self, *args, **options):
        #file_path = options['file_path']
        file_path = r"C:/Users/HP/Documents/OD management system/faculty details.xlsx"
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found!"))
            return

        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):  # Skip header
            faculty_code, full_name, faculty_type = row[1], row[2], row[3]

            if not faculty_code or not full_name or not faculty_type:
                print("skipped row",row)  # Print skipped row for debugging
                continue  # Skip empty rows

            # Split full name into first and last name
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # Determine faculty type
            if "HOD" in faculty_type:
                faculty_type = Faculty.FacultyType.HOD
            elif "Academic Head I" in faculty_type:
                faculty_type = Faculty.FacultyType.ACADEMIC_HEAD_1
            elif "Academic Head II" in faculty_type:
                faculty_type = Faculty.FacultyType.ACADEMIC_HEAD_2
            elif "Academic Head III" in faculty_type:
                faculty_type = Faculty.FacultyType.ACADEMIC_HEAD_3
            else:
                faculty_type = Faculty.FacultyType.TEACHING

            # Create User object
            user, created = User.objects.get_or_create(
                username=faculty_code,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name
                }
            )

            # Create Faculty object
            Faculty.objects.update_or_create(
                user=user,
                defaults={
                    "department": "CSE",
                    "faculty_code": faculty_code,
                    "faculty_type": faculty_type
                }
            )

            self.stdout.write(self.style.SUCCESS(f"Added/Updated: {full_name}"))

        self.stdout.write(self.style.SUCCESS("Faculty import completed successfully!"))
