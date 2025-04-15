import requests
from kivy.app import App
import json

BASE_URL = 'http://127.0.0.1:8000/api'  # Change to your Django backend URL

class APIClient:
    @staticmethod
    def get_headers():
        app = App.get_running_app()
        token = app.token_storage.get_token()
        if token:
            return {'Authorization': f'Bearer {token}'}
        return {}
    
    @staticmethod
    def login(username, password):
        url = f"{BASE_URL}/token/"
        response = requests.post(url, data={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def get_user_details():
        url = f"{BASE_URL}/users/me/"
        headers = APIClient.get_headers()
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    # Student-specific API calls
    @staticmethod
    def get_student_attendance():
        url = f"{BASE_URL}/attendance/my_attendance/"
        headers = APIClient.get_headers()
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return []
    
    # Faculty-specific API calls
    @staticmethod
    def get_faculty_courses():
        url = f"{BASE_URL}/courses/"
        headers = APIClient.get_headers()
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Filter courses where the faculty is the current user
            # This depends on how your API returns the data
            return response.json()
        return []
    
    @staticmethod
    def mark_attendance(course_id, student_id, date, status):
        url = f"{BASE_URL}/attendance/"
        headers = APIClient.get_headers()
        data = {
            'course': course_id,
            'student': student_id,
            'date': date,
            'status': status
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.status_code == 201
    
    # More API methods will be added as needed