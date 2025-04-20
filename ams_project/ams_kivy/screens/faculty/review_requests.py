from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder
import threading
from utils.api import APIClient
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

class ReviewRequestsScreen(Screen):
    def on_enter(self):
        # Load both correction and excuse requests
        threading.Thread(target=self.load_requests).start()

    def load_requests(self):
        try:
            corrections = APIClient.get_pending_correction_requests()
            excuses = APIClient.get_pending_excuse_requests()
            all_requests = [
                {"type": "Correction", **r} for r in corrections
            ] + [
                {"type": "Excuse", **r} for r in excuses
            ]
            Clock.schedule_once(lambda dt: self.populate_requests(all_requests), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error_dialog(f"Failed to load requests: {str(e)}"), 0)

    def populate_requests(self, requests_data):
        self.ids.requests_container.clear_widgets()
        if not requests_data:
            self.ids.requests_container.add_widget(Builder.template('NoRequestsLabel'))
            return
        for req in requests_data:
            item = Builder.template('ReviewRequestItem')
            item.request_id = req.get('id')
            item.request_type = req.get('type')
            item.ids.student_label.text = req.get('student_name', 'Unknown Student')
            item.ids.request_type.text = req.get('type')
            item.ids.request_message.text = req.get('message', '')
            item.ids.approve_btn.bind(
                on_release=lambda btn, req_id=req.get('id'), rtype=req.get('type'): self.update_request(req_id, rtype, True)
            )
            item.ids.reject_btn.bind(
                on_release=lambda btn, req_id=req.get('id'), rtype=req.get('type'): self.update_request(req_id, rtype, False)
            )
            self.ids.requests_container.add_widget(item)

    def update_request(self, request_id, request_type, approved):
        self.show_loading_dialog("Updating request...")
        threading.Thread(target=self.submit_update_request, args=(request_id, request_type, approved)).start()

    def submit_update_request(self, request_id, request_type, approved):
        try:
            success = APIClient.review_correction_request(request_id, approved, request_type)
            Clock.schedule_once(lambda dt: self.handle_update_result(success), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error_dialog(f"Update failed: {str(e)}"), 0)

    def handle_update_result(self, success):
        if self.dialog:
            self.dialog.dismiss()
        if success:
            self.show_success_dialog("Request updated successfully")
            threading.Thread(target=self.load_requests).start()
        else:
            self.show_error_dialog("Failed to update request")

    def show_loading_dialog(self, message):
        self.dialog = MDDialog(
            text=message,
            auto_dismiss=False
        )
        self.dialog.open()

    def show_error_dialog(self, message):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def show_success_dialog(self, message):
        self.dialog = MDDialog(
            title="Success",
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()
