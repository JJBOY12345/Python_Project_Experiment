from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from utils.api import APIClient
from kivy.app import App
import threading
from kivy.clock import Clock


class LoginScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    login_button = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.dialog = None
    
    def on_login_button_press(self):
        """Handle login button press"""
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.show_error_dialog("Please enter both username and password")
            return
        
        # Show loading indicator or disable button
        self.login_button.disabled = True
        
        # Use a thread to prevent UI blocking
        threading.Thread(target=self.perform_login, args=(username, password)).start()
    
    def perform_login(self, username, password):
        """Perform login in separate thread"""
        result = APIClient.login(username, password)

        from kivy.clock import Clock

        if result['success']:
            token_data = result['data']
            print("DEBUG: Received token_data:", token_data)  # 🐞 TEMP DEBUG

            if 'access' in token_data and 'refresh' in token_data:
                app = App.get_running_app()
                app.token_storage.save_token(token_data)

                # Get user data
                user_data = APIClient.get_user_details()
                if user_data:
                    app.token_storage.save_user_data(user_data)

                    # Navigate to the correct screen based on role
                    role = user_data.get('role', '')
                    Clock.schedule_once(lambda dt: self.navigate_to_role_screen(role), 0)
                else:
                    Clock.schedule_once(lambda dt: self.show_error_dialog("Failed to get user data"), 0)
            else:
                Clock.schedule_once(lambda dt: self.show_error_dialog("Login succeeded, but token missing 'access'/'refresh'"), 0)
        else:
            Clock.schedule_once(lambda dt: self.show_error_dialog(f"Login failed: {result['error']}"), 0)

        # Re-enable login button in main thread
        Clock.schedule_once(lambda dt: self.enable_login_button(), 0)

    def enable_login_button(self):
        """Re-enable login button"""
        self.login_button.disabled = False
    
    def navigate_to_role_screen(self, role):
        """Navigate to the appropriate screen based on role"""
        app = App.get_running_app()
        
        if role == 'student':
            from screens.student.dashboard import StudentDashboard
            if not app.manager.has_screen('student_dashboard'):
                app.manager.add_widget(StudentDashboard(name='student_dashboard'))
            app.manager.current = 'student_dashboard'
        
        elif role == 'faculty':
            from screens.faculty.dashboard import FacultyDashboard
            if not app.manager.has_screen('faculty_dashboard'):
                app.manager.add_widget(FacultyDashboard(name='faculty_dashboard'))
            app.manager.current = 'faculty_dashboard'
        
        elif role == 'admin':
            from screens.admin.dashboard import AdminDashboard
            if not app.manager.has_screen('admin_dashboard'):
                app.manager.add_widget(AdminDashboard(name='admin_dashboard'))
            app.manager.current = 'admin_dashboard'
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()