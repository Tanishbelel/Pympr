from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'subject', 'date']

class Marks(models.Model):
    EXAM_TYPES = [
        ('ISE1', 'First Internal'),
        ('MSE', 'Mid Semester'),
        ('ISE2', 'Second Internal'),
        ('ESE', 'End Semester'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=4, choices=EXAM_TYPES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ['student', 'subject', 'exam_type']

