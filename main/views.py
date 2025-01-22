from django.shortcuts import render, redirect,get_object_or_404

from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.db.models import Q
from django.db.models import Count

from django.http import JsonResponse
# Create your views here.


def home(request):
    return render(request , 'main.html')

def login_page(request):
    if request.method== "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
             messages.info(request, 'Invalid Data')
             return redirect('/login/')
        user = authenticate(username = username, password = password)

        if user is None:
             messages.info(request, 'Invalid Data')
             return redirect('/login/')
        else :
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')
    

def register_page(request):

    if request.method== "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already Taken')
            return redirect('/register/')

        user=User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()


        messages.info(request, 'Account Created Successfully')

        return redirect("/login/")

    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required
def dashboard(request):
    context = {
        'semester_progress': 65,
        'total_classes': 90,
        'classes_attended': 85,
        'overall_attendance': 94.4,
        'subjects': {
            'Mathematics': {
                'attendance': 85,
                'marks': {
                    'ISE 1': {'obtained': 5, 'total': 20},
                    'MSE': {'obtained': 24, 'total': 30},
                    'ISE 2': {'obtained': 14, 'total': 20},
                    'ESE': {'obtained': 24, 'total': 30},
                }
            },
            'Data-Structure': {
                'attendance': 75,
                'marks': {
                    'ISE 1': {'obtained': 12, 'total': 20},
                    'MSE': {'obtained': 82, 'total': 100},
                    'ISE 2': {'obtained': 8, 'total': 30},
                    'ESE': {'obtained': 80, 'total': 100},
                }
            },
            'Java': {
                'attendance': 90,
                'marks': {
                    'ISE 1': {'obtained': 12, 'total': 20},
                    'MSE': {'obtained': 82, 'total': 100},
                    'ISE 2': {'obtained': 8, 'total': 30},
                    'ESE': {'obtained': 80, 'total': 100},
                }
            },
            'Python': {
                'attendance': 90,
                'marks': {
                    'ISE 1': {'obtained': 12, 'total': 20},
                    'MSE': {'obtained': 82, 'total': 100},
                    'ISE 2': {'obtained': 8, 'total': 30},
                    'ESE': {'obtained': 80, 'total': 100},
                }
            },
            'React': {
                'attendance': 90,
                'marks': {
                    'ISE 1': {'obtained': 12, 'total': 20},
                    'MSE': {'obtained': 82, 'total': 100},
                    'ISE 2': {'obtained': 8, 'total': 30},
                    'ESE': {'obtained': 80, 'total': 100},
                }
            }
        },
        'user': request.user
    }
    return render(request, 'index.html', context)
        
@login_required
def attendance_page(request):
    total_classes = 90
    classes_attended = 85
    overall_attendance = 94.4
    classes_missed = total_classes - classes_attended  # Calculate missed classes here
    
    context = {
        'total_classes': total_classes,
        'classes_attended': classes_attended,
        'classes_missed': classes_missed,  # Add to context
        'overall_attendance': overall_attendance,
        'subjects': {
            'Mathematics': {'attendance': 35, 'classes_attended': 2, 'total_classes': 40},
            'Data-Structure': {'attendance': 75, 'classes_attended': 30, 'total_classes': 40},
            'Java': {'attendance': 90, 'classes_attended': 36, 'total_classes': 40},
            'Python': {'attendance': 90, 'classes_attended': 36, 'total_classes': 40},
            'React': {'attendance': 90, 'classes_attended': 36, 'total_classes': 40},
        }
    }
    return render(request, 'attendance.html', context)

@login_required
def marks_page(request):
    context = {
        'overall_percentage': 82.5,
        'subjects': {
            'Mathematics': {
                'marks': {
                    'ISE1': {'obtained': 18, 'total': 20, 'percentage': 90},
                    'MSE': {'obtained': 24, 'total': 30, 'percentage': 80},
                    'ISE2': {'obtained': 16, 'total': 20, 'percentage': 80},
                    'ESE': {'obtained': 24, 'total': 30, 'percentage': 80}
                },
                'total_obtained': 82,
                'total_marks': 100,
                'grade': 'A',
                'percentage': 82  # Added total percentage
            },
            'Data-Structure': {
                'marks': {
                    'ISE1': {'obtained': 15, 'total': 20, 'percentage': 75},
                    'MSE': {'obtained': 82, 'total': 100, 'percentage': 82},
                    'ISE2': {'obtained': 25, 'total': 30, 'percentage': 83.33},
                    'ESE': {'obtained': 80, 'total': 100, 'percentage': 80}
                },
                'total_obtained': 202,
                'total_marks': 250,
                'grade': 'A',
                'percentage': 80.8  # Added total percentage
            },
            'Java': {
                'marks': {
                    'ISE1': {'obtained': 16, 'total': 20, 'percentage': 80},
                    'MSE': {'obtained': 85, 'total': 100, 'percentage': 85},
                    'ISE2': {'obtained': 25, 'total': 30, 'percentage': 83.33},
                    'ESE': {'obtained': 85, 'total': 100, 'percentage': 85}
                },
                'total_obtained': 211,
                'total_marks': 250,
                'grade': 'A',
                'percentage': 84.4  # Added total percentage
            },
            'Python': {
                'marks': {
                    'ISE1': {'obtained': 18, 'total': 20, 'percentage': 90},
                    'MSE': {'obtained': 90, 'total': 100, 'percentage': 90},
                    'ISE2': {'obtained': 27, 'total': 30, 'percentage': 90},
                    'ESE': {'obtained': 88, 'total': 100, 'percentage': 88}
                },
                'total_obtained': 223,
                'total_marks': 250,
                'grade': 'A+',
                'percentage': 89.2  # Added total percentage
            },
            'React': {
                'marks': {
                    'ISE1': {'obtained': 17, 'total': 20, 'percentage': 85},
                    'MSE': {'obtained': 88, 'total': 100, 'percentage': 88},
                    'ISE2': {'obtained': 26, 'total': 30, 'percentage': 86.67},
                    'ESE': {'obtained': 85, 'total': 100, 'percentage': 85}
                },
                'total_obtained': 216,
                'total_marks': 250,
                'grade': 'A',
                'percentage': 86.4  # Added total percentage
            }
        }
    }

    # Calculate percentage for each subject
    for subject_data in context['subjects'].values():
        subject_data['percentage'] = (subject_data['total_obtained'] / subject_data['total_marks']) * 100

    return render(request, 'marks.html', context)