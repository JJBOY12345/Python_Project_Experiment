from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from users.models import UserProfile, Subject, Attendance
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from datetime import datetime

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("🔍 Received login data:", data)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == role:
                    return JsonResponse({'success': True, 'role': role})
                else:
                    return JsonResponse({'success': False, 'error': 'Role mismatch'})
            except UserProfile.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User profile not found'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def get_subjects(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()
        subject_list = [{'id': sub.id, 'code': sub.code, 'name': sub.name} for sub in subjects]
        return JsonResponse({'subjects': subject_list})
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

@csrf_exempt
def get_students(request):
    if request.method == 'GET':
        students = User.objects.filter(userprofile__role='student')
        student_list = [{'id': stu.id, 'username': stu.username} for stu in students]
        return JsonResponse({'students': student_list})
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject_id = data.get('subject_id')
            date_str = data.get('date')
            marked_by_id = data.get('marked_by_id')
            attendance_data = data.get('attendance_data')  # List of {student_id, status}
            
            # Convert date string to date object
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            subject = Subject.objects.get(id=subject_id)
            marked_by = User.objects.get(id=marked_by_id)
            
            # Check if attendance already exists for this subject and date
            existing = Attendance.objects.filter(subject=subject, date=date).exists()
            if existing:
                return JsonResponse({
                    'success': False, 
                    'error': 'Attendance already marked for this subject and date',
                    'exists': True
                })
            
            # Create attendance records
            created_records = []
            for record in attendance_data:
                student = User.objects.get(id=record['student_id'])
                attendance = Attendance(
                    student=student,
                    subject=subject,
                    date=date,
                    status=record['status'],
                    marked_by=marked_by
                )
                attendance.save()
                created_records.append({
                    'student_id': student.id,
                    'status': record['status']
                })
            
            return JsonResponse({
                'success': True,
                'message': f'Attendance marked for {len(created_records)} students',
                'records': created_records
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def get_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject_id = data.get('subject_id')
            date_str = data.get('date')
            
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            subject = Subject.objects.get(id=subject_id)
            
            attendance_records = Attendance.objects.filter(subject=subject, date=date)
            records = [{
                'student_id': record.student.id,
                'student_name': record.student.username,
                'status': record.status
            } for record in attendance_records]
            
            return JsonResponse({
                'success': True,
                'records': records,
                'exists': attendance_records.exists()
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
