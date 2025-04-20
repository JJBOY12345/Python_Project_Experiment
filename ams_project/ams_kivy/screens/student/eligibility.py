# Create screens/student/eligibility.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineIconListItem, TwoLineAvatarIconListItem, IconLeftWidget
import threading
from kivy.clock import Clock

class EligibilityScreen(Screen):
    eligibility_list = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(EligibilityScreen, self).__init__(**kwargs)
        self.dialog = None
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Show loading indicator
        self.show_loading_dialog()
        
        # Load eligibility data in a separate thread
        threading.Thread(target=self.load_eligibility_data).start()
    
    def load_eligibility_data(self):
        """Load eligibility data from API"""
        eligibility_data = APIClient.get_student_eligibility()
        
        # Update UI in the main thread
        Clock.schedule_once(lambda dt: self.update_eligibility_ui(eligibility_data), 0)
    
    def update_eligibility_ui(self, eligibility_data):
        """Update eligibility UI with the loaded data"""
        # Dismiss loading dialog
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        # Clear existing items
        if hasattr(self, 'eligibility_list') and self.eligibility_list:
            self.eligibility_list.clear_widgets()
            
            if eligibility_data and 'courses' in eligibility_data:
                for course in eligibility_data['courses']:
                    course_name = course.get('course_name', 'Unknown Course')
                    attendance_percentage = course.get('attendance_percentage', 0)
                    required_percentage = course.get('required_percentage', 75)
                    is_eligible = course.get('is_eligible', False)
                    
                    # Choose icon based on eligibility
                    icon = "check-circle" if is_eligible else "alert-circle"
                    
                    # Choose text color based on eligibility
                    if is_eligible:
                        status_text = f"Eligible ({attendance_percentage:.1f}% attendance)"
                    else:
                        status_text = f"Not Eligible ({attendance_percentage:.1f}% of required {required_percentage}%)"
                    
                    list_item = TwoLineAvatarIconListItem(
                        text=course_name,
                        secondary_text=status_text
                    )
                    list_item.add_widget(IconLeftWidget(icon=icon))
                    self.eligibility_list.add_widget(list_item)
            else:
                # No eligibility data
                no_data_item = OneLineIconListItem(
                    text="No eligibility information available",
                )
                no_data_item.add_widget(IconLeftWidget(icon="alert-circle"))
                self.eligibility_list.add_widget(no_data_item)
    
    def show_loading_dialog(self):
        """Show loading dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Loading",
            text="Please wait while we fetch your eligibility data...",
        )
        self.dialog.open()
    
    def go_back(self):
        """Navigate back to student dashboard"""
        app = App.get_running_app()
        app.manager.current = 'student_dashboard'