# In app.py, update the Builder.load_file section:
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp

from screens.login_screen import LoginScreen
from utils.storage import TokenStorage

# Import all KV files
Builder.load_file('kv/login_screen.kv')
Builder.load_file('kv/student/dashboard.kv')
Builder.load_file('kv/faculty/dashboard.kv')
Builder.load_file('kv/admin/dashboard.kv')

# Additional screen KV files
# Student screens
Builder.load_file('kv/student/attendance.kv')
Builder.load_file('kv/student/correction.kv')
Builder.load_file('kv/student/excuse.kv')
Builder.load_file('kv/student/eligibility.kv')
Builder.load_file('kv/notifications.kv')

# Faculty screens
Builder.load_file('kv/faculty/mark_attendance.kv')
Builder.load_file('kv/faculty/reports.kv')
Builder.load_file('kv/faculty/review_requests.kv')
Builder.load_file('kv/faculty/generate_reports.kv')

# Admin screens
Builder.load_file('kv/admin/user_management.kv')
Builder.load_file('kv/admin/analytics.kv')
Builder.load_file('kv/admin/attendance_tracking.kv')

class AMSApp(MDApp):
    manager = ObjectProperty(None)
    token_storage = ObjectProperty(None)
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        self.token_storage = TokenStorage()
        
        # Create the screen manager
        self.manager = ScreenManager()
        self.manager.add_widget(LoginScreen(name='login'))
        
        # Check if there's a saved token
        token = self.token_storage.get_token()
        if token:
            # Validate token and navigate to appropriate screen
            user_data = self.token_storage.get_user_data()
            if user_data:
                role = user_data.get('role', '')
                # Lazy load the proper dashboard based on role
                if role == 'student':
                    from screens.student.dashboard import StudentDashboard
                    self.manager.add_widget(StudentDashboard(name='student_dashboard'))
                    self.manager.current = 'student_dashboard'
                elif role == 'faculty':
                    from screens.faculty.dashboard import FacultyDashboard
                    self.manager.add_widget(FacultyDashboard(name='faculty_dashboard'))
                    self.manager.current = 'faculty_dashboard'
                elif role == 'admin':
                    from screens.admin.dashboard import AdminDashboard
                    self.manager.add_widget(AdminDashboard(name='admin_dashboard'))
                    self.manager.current = 'admin_dashboard'
            
        return self.manager