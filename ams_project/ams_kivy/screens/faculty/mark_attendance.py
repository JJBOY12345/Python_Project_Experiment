# ams_kivy/screens/faculty/mark_attendance.py

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from utils.api import APIClient
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    OneLineAvatarIconListItem, CheckboxLeftWidget, OneLineListItem
)
import threading
from datetime import datetime

class AttendanceListItem(OneLineAvatarIconListItem):
    """Custom list item with checkbox for marking attendance"""
    def __init__(self, student_id=None, **kwargs):
        super().__init__(**kwargs)
        self.student_id = student_id
        self.checkbox = CheckboxLeftWidget()
        self.add_widget(self.checkbox)

class MarkAttendanceScreen(Screen):
    course_dropdown     = ObjectProperty(None)
    date_picker_button  = ObjectProperty(None)
    students_list       = ObjectProperty(None)
    submit_button       = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.courses = []
        self.student_items = []
        self.selected_course = None
        self.selected_date = None
        self.course_menu = None

    def on_enter(self):
        self.show_loading_dialog("Loading courses...")
        threading.Thread(target=self.load_courses, daemon=True).start()

    def load_courses(self):
        resp = APIClient.get_faculty_courses()
        if resp.get('success'):
            self.courses = resp['data']
            Clock.schedule_once(lambda dt: self.update_courses_ui(), 0)
        else:
            Clock.schedule_once(lambda dt: self.show_error_dialog(resp.get('error')), 0)

    def update_courses_ui(self):
        if self.dialog:
            self.dialog.dismiss()

        # Build dropdown menu
        items = [{
            "text": f"{c['course_code']} - {c['course_name']}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=c: self.set_course(x)
        } for c in self.courses]

        self.course_menu = MDDropdownMenu(
            caller=self.course_dropdown,
            items=items,
            width_mult=4
        )

    def open_course_menu(self):
        if self.course_menu:
            self.course_menu.open()
        else:
            self.show_error_dialog("Course menu not yet available")

    def set_course(self, course):
        self.selected_course = course
        self.course_dropdown.text = f"{course['course_code']} - {course['course_name']}"
        self.course_menu.dismiss()

        if self.selected_date:
            self.load_students(course['id'])

    def show_date_picker(self):
        dp = MDDatePicker(
            max_date=datetime.now().date(),
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        dp.bind(on_save=self.on_date_save)
        dp.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        self.date_picker_button.text = value.strftime("%d %b, %Y")
        if self.selected_course:
            self.load_students(self.selected_course['id'])

    def load_students(self, course_id):
        self.show_loading_dialog("Loading students...")
        threading.Thread(target=self._load_students_thread, args=(course_id,), daemon=True).start()

    def _load_students_thread(self, course_id):
        resp = APIClient.get_course_students(course_id)
        if resp.get('success'):
            self.students = resp['data']
            Clock.schedule_once(lambda dt: self.update_students_ui(), 0)
        else:
            Clock.schedule_once(lambda dt: self.show_error_dialog(resp.get('error')), 0)

    def update_students_ui(self):
        if self.dialog:
            self.dialog.dismiss()

        self.ids.students_list.clear_widgets()  # Use `self.ids` instead of `self.students_list`
        self.student_items = []

        if not self.students:
            self.ids.students_list.add_widget(
                OneLineAvatarIconListItem(text="No students enrolled in this course")
            )
            self.ids.submit_button.disabled = True  # Use `self.ids` to access buttons too
            return

        for enrollment in self.students:
            name = enrollment.get('student_name', 'Unknown')
            sid = enrollment.get('student')  # This should be the student ID
            item = AttendanceListItem(
                text=name,
                student_id=sid
            )
            item.checkbox.active = True
            self.ids.students_list.add_widget(item)
            self.student_items.append(item)

        self.ids.submit_button.disabled = False

    def submit_attendance(self):
        if not (self.selected_course and self.selected_date):
            self.show_error_dialog("Select course & date first")
            return

        records = [{
            'student': itm.student_id,
            'status': 'present' if itm.checkbox.active else 'absent'
        } for itm in self.student_items]

        payload = {
            'course_id': self.selected_course['id'],
            'date': self.selected_date.strftime('%Y-%m-%d'),
            'records': records
        }

        self.show_loading_dialog("Submitting attendance...")
        threading.Thread(target=self._submit_thread, args=(payload,), daemon=True).start()

    def _submit_thread(self, data):
        resp = APIClient.mark_attendance(data)
        Clock.schedule_once(lambda dt: self._after_submit(resp), 0)

    def _after_submit(self, resp):
        self.dismiss_loading_dialog()
        if resp.get('success'):
            self.show_success_dialog("Attendance recorded!")
            self.go_back()
        else:
            self.show_error_dialog(resp.get('error'))

    # ────────────────────────────────────────────────────────────────────────────────
    # Helper dialogs
    def show_loading_dialog(self, message):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        if not message:
            message = "Loading..."

        spinner = MDSpinner(size_hint=(None, None), size=(48, 48))
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(spinner)
        content.add_widget(MDLabel(text=message[:300], halign='center'))  # Truncate just in case

        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            auto_dismiss=False
        )
        self.dialog.open()

    def dismiss_loading_dialog(self):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def show_error_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()

        if not message:
            message = "Unknown error"

        if len(message) > 500:
            print("[ERROR] Message too long for dialog. Logging instead:")
            print(message)
            message = "An unexpected error occurred. Please check logs."

        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda _: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def show_success_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda d: self.dialog.dismiss())]
        )
        self.dialog.open()

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'faculty_dashboard'
