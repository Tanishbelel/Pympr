# admin.py
from django.contrib import admin
from .models import Student, Subject, Attendance, Marks

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'semester')
    search_fields = ('roll_number', 'user__username')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'present')
    list_filter = ('present', 'subject', 'date')
    search_fields = ('student__roll_number', 'subject__name')
    date_hierarchy = 'date'

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_type', 'marks_obtained', 'total_marks')
    list_filter = ('exam_type', 'subject')
    search_fields = ('student__roll_number', 'subject__name')