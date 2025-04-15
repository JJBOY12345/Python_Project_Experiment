from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient

class FacultyDashboard(Screen):
    name_label = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(FacultyDashboard, self).__init__(**kwargs)
    
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
    
    def mark_attendance(self):
        """Navigate to mark attendance screen"""
        app = App.get_running_app()
        from screens.faculty.mark_attendance import MarkAttendanceScreen
        
        if not app.manager.has_screen('mark_attendance'):
            app.manager.add_widget(MarkAttendanceScreen(name='mark_attendance'))
        
        app.manager.current = 'mark_attendance'
    
    def view_reports(self):
        """Navigate to attendance reports screen"""
        app = App.get_running_app()
        from screens.faculty.reports import AttendanceReportsScreen
        
        if not app.manager.has_screen('attendance_reports'):
            app.manager.add_widget(AttendanceReportsScreen(name='attendance_reports'))
        
        app.manager.current = 'attendance_reports'
    
    def review_requests(self):
        """Navigate to review requests screen"""
        app = App.get_running_app()
        from screens.faculty.review_requests import ReviewRequestsScreen
        
        if not app.manager.has_screen('review_requests'):
            app.manager.add_widget(ReviewRequestsScreen(name='review_requests'))
        
        app.manager.current = 'review_requests'
    
    def generate_reports(self):
        """Navigate to generate reports screen"""
        app = App.get_running_app()
        from screens.faculty.generate_reports import GenerateReportsScreen
        
        if not app.manager.has_screen('generate_reports'):
            app.manager.add_widget(GenerateReportsScreen(name='generate_reports'))
        
        app.manager.current = 'generate_reports'