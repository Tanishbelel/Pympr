# yourapp/management/commands/setup_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from main.models import Student, Subject, Attendance, Marks
import random

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Create test user and student
        user = User.objects.create_user(
            username='test_student',
            password='test123',
            first_name='Test',
            last_name='Student'
        )
        
        student = Student.objects.create(
            user=user,
            roll_number='2023CS001',
            semester=3
        )

        # Create subjects
        subjects = [
            Subject.objects.create(name='Mathematics', code='MATH301'),
            Subject.objects.create(name='Data-Structure', code='CS302'),
            Subject.objects.create(name='Java', code='CS303'),
            Subject.objects.create(name='Python', code='CS304'),
            Subject.objects.create(name='React', code='CS305')
        ]

        # Create attendance records for the last 3 months
        start_date = timezone.now().date() - timedelta(days=90)
        for subject in subjects:
            for i in range(90):
                if i % 7 not in [5, 6]:  # No classes on weekends
                    date = start_date + timedelta(days=i)
                    # Random attendance with 85% probability of being present
                    present = random.random() < 0.85
                    Attendance.objects.create(
                        student=student,
                        subject=subject,
                        date=date,
                        present=present
                    )

        # Create marks for each subject
        exam_types = ['ISE1', 'MSE', 'ISE2', 'ESE']
        max_marks = {'ISE1': 20, 'MSE': 100, 'ISE2': 30, 'ESE': 100}
        
        for subject in subjects:
            for exam_type in exam_types:
                total_marks = max_marks[exam_type]
                # Random marks with minimum 60% score
                obtained_marks = random.uniform(0.6 * total_marks, total_marks)
                Marks.objects.create(
                    student=student,
                    subject=subject,
                    exam_type=exam_type,
                    marks_obtained=round(obtained_marks, 2),
                    total_marks=total_marks
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))