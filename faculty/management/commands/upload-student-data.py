import os
import openpyxl
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student.models import Student

class Command(BaseCommand):
    help = "Import faculty data from an Excel file"

    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', type=str, help="Path to the Excel file")

    def handle(self, *args, **options):
        #file_path = options['file_path']
        file_path = r"C:/Users/HP/Documents/OD management system/student-details.xlsx"
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found!"))
            return

        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        for row in ws.iter_rows(min_row=3, values_only=True):  # Skip header
            student_name, roll_no, section = row[2], row[3], row[4]
            if not student_name or not roll_no or not section:
                print("skipped row",row)  # Print skipped row for debugging
                continue  # Skip empty rows

            # Split full name into first and last name
            name_parts = student_name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # Determine faculty type
            
            # Create User object
            user, created = User.objects.get_or_create(
                username=roll_no,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name
                }
            )

            # Create Faculty object
            Student.objects.update_or_create(
                user=user,
                defaults={
                    "department": "CSE",
                    "year": 2,
                    "roll_number": roll_no,
                    "section": section,
                }
            )

            self.stdout.write(self.style.SUCCESS(f"Added/Updated: {student_name}"))

        self.stdout.write(self.style.SUCCESS("Faculty import completed successfully!"))
