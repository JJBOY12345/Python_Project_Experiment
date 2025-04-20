from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineIconListItem, TwoLineAvatarIconListItem, IconLeftWidget
import threading
from kivy.clock import Clock
from datetime import datetime

class StudentAttendanceScreen(Screen):
    attendance_list = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(StudentAttendanceScreen, self).__init__(**kwargs)
        self.dialog = None
        self.attendance_data = []
        
    def on_enter(self):
        """Called when the screen is entered"""
        # Show loading indicator
        self.show_loading_dialog()
        
        # Load attendance data in a separate thread
        threading.Thread(target=self.load_attendance_data).start()
    
    def load_attendance_data(self):
        """Load attendance data from API"""
        attendance_data = APIClient.get_student_attendance()
        
        # Calculate attendance percentage
        present_count = sum(1 for item in attendance_data if item.get('status') == 'present')
        total_count = len(attendance_data) if attendance_data else 0
        attendance_percentage = (present_count / total_count * 100) if total_count > 0 else 0
        
        # Store data for later use
        self.attendance_data = attendance_data
        
        # Update UI in the main thread
        Clock.schedule_once(lambda dt: self.update_attendance_ui(attendance_data, attendance_percentage), 0)
    
    def update_attendance_ui(self, attendance_data, attendance_percentage):
        """Update attendance UI with the loaded data"""
        # Dismiss loading dialog
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        # Clear existing items
        if hasattr(self, 'attendance_list') and self.attendance_list:
            self.attendance_list.clear_widgets()
            
            # Add attendance percentage
            percentage_item = OneLineIconListItem(
                text=f"Overall Attendance: {attendance_percentage:.1f}%",
            )
            percentage_item.add_widget(IconLeftWidget(icon="percent"))
            self.attendance_list.add_widget(percentage_item)
            
            # Add attendance records
            if attendance_data:
                for item in attendance_data:
                    status = item.get('status', 'unknown')
                    date = item.get('date', '')
                    course = item.get('course', {}).get('course_name', '')
                    
                    # Format date
                    try:
                        date_obj = datetime.strptime(date, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%d %b, %Y")
                    except:
                        formatted_date = date
                    
                    # Choose icon based on status
                    icon = "check-circle" if status == 'present' else "close-circle"
                    
                    list_item = TwoLineAvatarIconListItem(
                        text=f"{course}",
                        secondary_text=f"{formatted_date} - {status.capitalize()}"
                    )
                    list_item.add_widget(IconLeftWidget(icon=icon))
                    self.attendance_list.add_widget(list_item)
            else:
                # No attendance data
                no_data_item = OneLineIconListItem(
                    text="No attendance records found",
                )
                no_data_item.add_widget(IconLeftWidget(icon="alert-circle"))
                self.attendance_list.add_widget(no_data_item)
    
    def show_loading_dialog(self):
        """Show loading dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Loading",
            text="Please wait while we fetch your attendance data...",
        )
        self.dialog.open()
    
    def go_back(self):
        """Navigate back to student dashboard"""
        app = App.get_running_app()
        app.manager.current = 'student_dashboard'