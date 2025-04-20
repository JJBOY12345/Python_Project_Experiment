import requests
from kivy.app import App
import json
import logging

BASE_URL = 'http://127.0.0.1:8000/api'  # Backend URL

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def get_headers():
        try:
            app = App.get_running_app()
            token = app.token_storage.get_token()
            if token:
                return {'Authorization': f'Bearer {token}'}
        except Exception as e:
            logger.error(f"Error getting headers: {e}")
        return {}

    @staticmethod
    def login(username, password):
        url = url = f"{BASE_URL}/token/"  
        headers = {'Content-Type': 'application/json'}
        payload = {"username": username, "password": password}
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.text}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def refresh_token(refresh_token):
        url = f"{BASE_URL}/token/refresh/"
        try:
            response = requests.post(url, data={'refresh': refresh_token}, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Token refresh failed')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_user_details():
        url = f"{BASE_URL}/users/me/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch user details')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_student_attendance():
        url = f"{BASE_URL}/attendance/my_attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch attendance')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_student_courses():
        url = f"{BASE_URL}/courses/my_courses/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch courses')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def submit_correction_request(data):
        url = f"{BASE_URL}/correction-requests/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code in (200, 201):
                return {"success": True, "data": None, "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to submit correction request')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def submit_excuse_request(data):
        url = f"{BASE_URL}/excuse-requests/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code in (200, 201):
                return {"success": True, "data": None, "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to submit excuse request')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_student_eligibility():
        url = f"{BASE_URL}/students/eligibility/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch eligibility')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_faculty_courses():
        url = f"{BASE_URL}/courses/teaching/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch faculty courses')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_course_students(course_id):
        url = f"{BASE_URL}/courses/{course_id}/students/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch course students')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def mark_attendance(course_id, date, attendance_records):
        """Mark attendance for a course on a date"""
        url = f"{BASE_URL}/attendance/batch_mark/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'  # Add this line
        payload = {
            "course_id": course_id,
            "date": date,
            "records": attendance_records
        }   
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in (200, 201):
                return {"success": True, "data": None, "error": None}
            return {"success": False, "data": None, "error": response.text}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_pending_correction_requests():
        url = f"{BASE_URL}/correction-requests/pending_reviews/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch pending correction requests')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_pending_excuse_requests():
        url = f"{BASE_URL}/excuse-requests/pending_reviews/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch pending excuse requests')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def review_correction_request(request_id, approved, comment):
        url = f"{BASE_URL}/correction-requests/{request_id}/review/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        data = {
            'approved': approved,
            'review_comment': comment
        }
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code in (200, 202):
                return {"success": True, "data": None, "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to review correction request')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_users():
        url = f"{BASE_URL}/users/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch users')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def create_user(user_data):
        url = f"{BASE_URL}/users/"
        headers = APIClient.get_headers()
        headers['Content-Type'] = 'application/json'
        try:
            response = requests.post(url, json=user_data, headers=headers, timeout=10)
            if response.status_code == 201:
                return {"success": True, "data": None, "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to create user')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_attendance_analytics():
        url = f"{BASE_URL}/analytics/attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch attendance analytics')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}

    @staticmethod
    def get_low_attendance_students():
        url = f"{BASE_URL}/analytics/low_attendance/"
        headers = APIClient.get_headers()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "error": None}
            return {"success": False, "data": None, "error": response.json().get('detail', 'Failed to fetch low attendance students')}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}
