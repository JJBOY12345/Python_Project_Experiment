from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp

from screens.login_screen import LoginScreen
from utils.storage import TokenStorage

# Import all KV files
Builder.load_file('kv/login_screen.kv')
# We'll add more Builder.load_file calls as we create more KV files

class AMSApp(MDApp):
    manager = ObjectProperty(None)
    token_storage = ObjectProperty(None)
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        self.token_storage = TokenStorage()
        
        # Create the screen manager
        self.manager = ScreenManager()
        self.manager.add_widget(LoginScreen(name='login'))
        
        # Check if there's a saved token
        token = self.token_storage.get_token()
        if token:
            # Validate token and navigate to appropriate screen
            # For now, just go to login
            return self.manager
        
        return self.manager