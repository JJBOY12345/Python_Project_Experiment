# Create screens/notifications.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from utils.api import APIClient
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget
import threading
from kivy.clock import Clock
from datetime import datetime

class NotificationsScreen(Screen):
    notifications_list = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(NotificationsScreen, self).__init__(**kwargs)
        self.dialog = None
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Show loading indicator
        self.show_loading_dialog()
        
        # Get the user role
        app = App.get_running_app()
        role = app.token_storage.get_user_role()
        
        # Load notifications data in a separate thread
        threading.Thread(target=self.load_notifications_data, args=(role,)).start()
    
    def load_notifications_data(self, role):
        """Load notifications data from API"""
        # Use different API endpoints based on role
        notifications = []
        
        if role == 'student':
            notifications = APIClient.get_student_notifications()
        elif role == 'faculty':
            notifications = APIClient.get_faculty_notifications()
        elif role == 'admin':
            notifications = APIClient.get_admin_notifications()
        
        # Update UI in the main thread
        Clock.schedule_once(lambda dt: self.update_notifications_ui(notifications), 0)
    
    def update_notifications_ui(self, notifications):
        """Update notifications UI with the loaded data"""
        # Dismiss loading dialog
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        # Clear existing items
        if hasattr(self, 'notifications_list') and self.notifications_list:
            self.notifications_list.clear_widgets()
            
            if notifications:
                for notification in notifications:
                    title = notification.get('title', 'Notification')
                    message = notification.get('message', '')
                    date_str = notification.get('date', '')
                    is_read = notification.get('is_read', False)
                    
                    # Format date
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                        formatted_date = date_obj.strftime("%d %b, %Y %H:%M")
                    except:
                        formatted_date = date_str
                    
                    # Choose icon based on read status
                    icon = "email-open" if is_read else "email"
                    
                    list_item = TwoLineAvatarIconListItem(
                        text=title,
                        secondary_text=f"{message} - {formatted_date}"
                    )
                    list_item.add_widget(IconLeftWidget(icon=icon))
                    self.notifications_list.add_widget(list_item)
            else:
                # No notifications
                no_notifications_item = TwoLineAvatarIconListItem(
                    text="No notifications",
                    secondary_text="You don't have any notifications at this time"
                )
                no_notifications_item.add_widget(IconLeftWidget(icon="bell-outline"))
                self.notifications_list.add_widget(no_notifications_item)
    
    def show_loading_dialog(self):
        """Show loading dialog"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Loading",
            text="Please wait while we fetch your notifications...",
        )
        self.dialog.open()
    
    def go_back(self):
        """Navigate back to user's dashboard based on role"""
        app = App.get_running_app()
        role = app.token_storage.get_user_role()
        
        if role == 'student':
            app.manager.current = 'student_dashboard'
        elif role == 'faculty':
            app.manager.current = 'faculty_dashboard'
        elif role == 'admin':
            app.manager.current = 'admin_dashboard'
        else:
            app.manager.current = 'login'