from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget

class StudentDashboard(Screen):
    name_label = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(StudentDashboard, self).__init__(**kwargs)
        self.dialog = None
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Update user name
        app = App.get_running_app()
        user_data = app.token_storage.get_user_data()
        if user_data:
            full_name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}"
            self.name_label.text = f"Welcome, {full_name}"
    
    def logout(self):
        """Handle logout button press"""
        app = App.get_running_app()
        app.token_storage.clear_tokens()
        app.manager.current = 'login'
    
    def view_attendance(self):
        """Navigate to attendance screen"""
        app = App.get_running_app()
        from screens.student.attendance import StudentAttendanceScreen
        
        if not app.manager.has_screen('student_attendance'):
            app.manager.add_widget(StudentAttendanceScreen(name='student_attendance'))
        
        app.manager.current = 'student_attendance'
    
    def submit_correction(self):
        """Navigate to attendance correction screen"""
        app = App.get_running_app()
        from screens.student.correction import CorrectionRequestScreen
        
        if not app.manager.has_screen('correction_request'):
            app.manager.add_widget(CorrectionRequestScreen(name='correction_request'))
        
        app.manager.current = 'correction_request'
    
    def excuse_absence(self):
        """Navigate to excuse absence screen"""
        app = App.get_running_app()
        from screens.student.excuse import ExcuseRequestScreen
        
        if not app.manager.has_screen('excuse_request'):
            app.manager.add_widget(ExcuseRequestScreen(name='excuse_request'))
        
        app.manager.current = 'excuse_request'
    
    def check_eligibility(self):
        """Navigate to eligibility screen"""
        app = App.get_running_app()
        from screens.student.eligibility import EligibilityScreen
        
        if not app.manager.has_screen('eligibility'):
            app.manager.add_widget(EligibilityScreen(name='eligibility'))
        
        app.manager.current = 'eligibility'
    
    def view_notifications(self):
        """Navigate to notifications screen"""
        app = App.get_running_app()
        from screens.notifications import NotificationsScreen
        
        if not app.manager.has_screen('notifications'):
            app.manager.add_widget(NotificationsScreen(name='notifications'))
        
        app.manager.current = 'notifications'