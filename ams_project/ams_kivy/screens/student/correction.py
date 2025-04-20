from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
import threading
from kivy.clock import Clock
from datetime import datetime

class CorrectionRequestScreen(Screen):
    course_dropdown = ObjectProperty(None)
    date_picker_button = ObjectProperty(None)
    reason_input = ObjectProperty(None)
    status_dropdown = ObjectProperty(None)
    submit_button = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(CorrectionRequestScreen, self).__init__(**kwargs)
        self.dialog = None
        self.courses = []
        self.selected_course = None
        self.selected_date = None
        self.selected_status = None
        self.course_menu = None
        self.status_menu = None
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Show loading indicator
        self.show_loading_dialog("Loading courses...")
        
        # Load courses in a separate thread
        threading.Thread(target=self.load_courses).start()
    
    def load_courses(self):
        """Load courses from API"""
        courses = APIClient.get_student_courses()
        
        # Store data for later use
        self.courses = courses
        
        # Update UI in the main thread
        Clock.schedule_once(lambda dt: self.update_courses_ui(courses), 0)
    
    def update_courses_ui(self, courses):
        """Update courses UI with the loaded data"""
        # Dismiss loading dialog
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        
        # Populate course dropdown
        course_items = [
            {
                "text": f"{course.get('course_code')} - {course.get('course_name')}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=course: self.set_course(x),
            } for course in courses
        ]
        
        # Create dropdown menu
        if self.course_menu:
            self.course_menu.dismiss()
            
        self.course_menu = MDDropdownMenu(
            caller=self.course_dropdown,
            items=course_items,
            width_mult=4,
        )
        
        # Create status dropdown
        status_items = [
            {
                "text": "Present",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="present": self.set_status(x),
            },
            {
                "text": "Absent",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="absent": self.set_status(x),
            }
        ]
        
        self.status_menu = MDDropdownMenu(
            caller=self.status_dropdown,
            items=status_items,
            width_mult=4,
        )
    
    def set_course(self, course):
        """Set selected course"""
        self.selected_course = course
        self.course_dropdown.text = f"{course.get('course_code')} - {course.get('course_name')}"
        self.course_menu.dismiss()
    
    def set_status(self, status):
        """Set selected status"""
        self.selected_status = status
        self.status_dropdown.text = status.capitalize()
        self.status_menu.dismiss()
    
    def show_date_picker(self):
        """Show date picker dialog"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()
    
    def on_date_save(self, instance, value, date_range):
        """Handle date selection"""
        self.selected_date = value
        self.date_picker_button.text = value.strftime("%d %b, %Y")
    
    def submit_correction(self):
        """Submit correction request"""
        if not self.selected_course or not self.selected_date or not self.selected_status:
            self.show_error_dialog("Please select a course, date, and status for correction")
            return
        
        reason = self.reason_input.text
        if not reason:
            self.show_error_dialog("Please provide a reason for the correction")
            return
        
        # Show loading indicator
        self.show_loading_dialog("Submitting request...")
        
        # Submit in a separate thread
        correction_data = {
            'course': self.selected_course.get('id'),
            'date': self.selected_date.strftime("%Y-%m-%d"),
            'requested_status': self.selected_status,
            'reason': reason
        }
        
        threading.Thread(target=self.submit_correction_request, args=(correction_data,)).start()
    
    def submit_correction_request(self, correction_data):
        """Submit correction request to API"""
        success = APIClient.submit_correction_request(correction_data)
        
        # Update UI in the main thread
        Clock.schedule_once(lambda dt: self.handle_submission_result(success), 0)
    
    def handle_submission_result(self, success):
        """Handle submission result"""
        # Dismiss loading dialog
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        
        if success:
            # Show success dialog
            self.show_success_dialog("Correction request submitted successfully")
        else:
            # Show error dialog
            self.show_error_dialog("Failed to submit correction request")
    
    def show_loading_dialog(self, message):
        """Show loading dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Please wait",
            text=message,
        )
        self.dialog.open()
    
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
    
    def show_success_dialog(self, message):
        """Show success dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_success_dialog_close()
                )
            ]
        )
        self.dialog.open()
    
    def handle_success_dialog_close(self):
        """Handle success dialog close"""
        if self.dialog:
            self.dialog.dismiss()
        
        # Go back to student dashboard
        app = App.get_running_app()
        app.manager.current = 'student_dashboard'
    
    def go_back(self):
        """Navigate back to student dashboard"""
        app = App.get_running_app()
        app.manager.current = 'student_dashboard'