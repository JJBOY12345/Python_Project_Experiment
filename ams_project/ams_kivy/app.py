from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp

from screens.login_screen import LoginScreen
from utils.storage import TokenStorage

# Load only existing KV files
Builder.load_file('kv/login_screen.kv')

# Student screens
Builder.load_file('kv/student/dashboard.kv')
Builder.load_file('kv/student/attendance.kv')
Builder.load_file('kv/student/correction.kv')

# Faculty screens
Builder.load_file('kv/faculty/dashboard.kv')
Builder.load_file('kv/faculty/mark_attendance.kv')
Builder.load_file('kv/faculty/review_requests.kv')

class AMSApp(MDApp):
    manager = ObjectProperty(None)
    token_storage = ObjectProperty(None)
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        self.token_storage = TokenStorage()
        
        self.manager = ScreenManager()
        self.manager.add_widget(LoginScreen(name='login'))
        
        token = self.token_storage.get_token()
        if token:
            user_data = self.token_storage.get_user_data()
            if user_data:
                role = user_data.get('role', '')
                if role == 'student':
                    from screens.student.dashboard import StudentDashboard
                    self.manager.add_widget(StudentDashboard(name='student_dashboard'))
                    self.manager.current = 'student_dashboard'
                elif role == 'faculty':
                    from screens.faculty.dashboard import FacultyDashboard
                    self.manager.add_widget(FacultyDashboard(name='faculty_dashboard'))
                    self.manager.current = 'faculty_dashboard'
                elif role == 'admin':
                    # If admin screen isn't ready yet, keep them on login or show a placeholder
                    from screens.admin.dashboard import AdminDashboard
                    self.manager.add_widget(AdminDashboard(name='admin_dashboard'))
                    self.manager.current = 'admin_dashboard'
        
        return self.manager
