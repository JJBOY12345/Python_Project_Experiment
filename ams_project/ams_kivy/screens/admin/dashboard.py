from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient

class AdminDashboard(Screen):
    name_label = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(AdminDashboard, self).__init__(**kwargs)
    
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
    
    def manage_users(self):
        """Navigate to user management screen"""
        app = App.get_running_app()
        from screens.admin.user_management import UserManagementScreen
        
        if not app.manager.has_screen('user_management'):
            app.manager.add_widget(UserManagementScreen(name='user_management'))
        
        app.manager.current = 'user_management'
    
    def generate_analytics(self):
        """Navigate to analytics screen"""
        app = App.get_running_app()
        from screens.admin.analytics import AnalyticsScreen
        
        if not app.manager.has_screen('analytics'):
            app.manager.add_widget(AnalyticsScreen(name='analytics'))
        
        app.manager.current = 'analytics'
    
    def track_attendance(self):
        """Navigate to attendance tracking screen"""
        app = App.get_running_app()
        from screens.admin.attendance_tracking import AttendanceTrackingScreen
        
        if not app.manager.has_screen('attendance_tracking'):
            app.manager.add_widget(AttendanceTrackingScreen(name='attendance_tracking'))
        
        app.manager.current = 'attendance_tracking'