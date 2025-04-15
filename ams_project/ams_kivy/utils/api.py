import requests
from kivy.app import App
import json

BASE_URL = 'http://127.0.0.1:8000/api'  # Change to your Django backend URL

class APIClient:
    @staticmethod
    def get_headers():
        """Get authorization headers with JWT token"""
        try:
            app = App.get_running_app()
            token = app.token_storage.get_token()
            if token:
                return {'Authorization': f'Bearer {token}'}
        except:
            pass
        return {}
    
    @staticmethod
    def login(username, password):
        """Login user and get JWT token"""
        url = f"{BASE_URL}/token/"
        try:
            response = requests.post(url, data={
                'username': username,
                'password': password
            }, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None
    
    @staticmethod
    def get_user_details():
        """Get current user details"""
        url = f"{BASE_URL}/users/me/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None
    
    # Student-specific API calls
    @staticmethod
    def get_student_attendance():
        """Get student's attendance records"""
        url = f"{BASE_URL}/attendance/my_attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def get_student_courses():
        """Get student's enrolled courses"""
        url = f"{BASE_URL}/courses/my_courses/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def submit_correction_request(data):
        """Submit attendance correction request"""
        url = f"{BASE_URL}/correction-requests/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code in (200, 201)
        except requests.exceptions.RequestException:
            pass
        return False
    
    @staticmethod
    def submit_excuse_request(data):
        """Submit absence excuse request"""
        url = f"{BASE_URL}/excuse-requests/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code in (200, 201)
        except requests.exceptions.RequestException:
            pass
        return False
    
    @staticmethod
    def get_student_eligibility():
        """Get student's eligibility status"""
        url = f"{BASE_URL}/students/eligibility/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None
    
    # Faculty-specific API calls
    @staticmethod
    def get_faculty_courses():
        """Get faculty's courses"""
        url = f"{BASE_URL}/courses/teaching/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def get_course_students(course_id):
        """Get students enrolled in a course"""
        url = f"{BASE_URL}/courses/{course_id}/students/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def mark_attendance(course_id, date, attendance_data):
        """Mark attendance for multiple students"""
        url = f"{BASE_URL}/attendance/batch_mark/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        
        data = {
            'course': course_id,
            'date': date,
            'attendance_records': attendance_data
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            return response.status_code in (200, 201)
        except requests.exceptions.RequestException:
            pass
        return False
    
    @staticmethod
    def get_pending_correction_requests():
        """Get pending correction requests for faculty review"""
        url = f"{BASE_URL}/correction-requests/pending_reviews/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def get_pending_excuse_requests():
        """Get pending excuse requests for faculty review"""
        url = f"{BASE_URL}/excuse-requests/pending_reviews/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def review_correction_request(request_id, approved, comment):
        """Review a correction request"""
        url = f"{BASE_URL}/correction-requests/{request_id}/review/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        
        data = {
            'approved': approved,
            'review_comment': comment
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code in (200, 202)
        except requests.exceptions.RequestException:
            pass
        return False
    
    # Admin-specific API calls
    @staticmethod
    def get_users():
        """Get all users (admin only)"""
        url = f"{BASE_URL}/users/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []
    
    @staticmethod
    def create_user(user_data):
        """Create a new user (admin only)"""
        url = f"{BASE_URL}/users/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        
        try:
            response = requests.post(url, json=user_data, headers=headers, timeout=10)
            return response.status_code == 201
        except requests.exceptions.RequestException:
            pass
        return False
    
    @staticmethod
    def get_attendance_analytics():
        """Get attendance analytics (admin only)"""
        url = f"{BASE_URL}/analytics/attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None
    
    @staticmethod
    def get_low_attendance_students():
        """Get students with low attendance (admin only)"""
        url = f"{BASE_URL}/analytics/low_attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []