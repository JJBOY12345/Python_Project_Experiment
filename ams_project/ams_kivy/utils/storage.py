from kivy.storage.jsonstore import JsonStore
from os.path import join
from kivy.app import App

class TokenStorage:
    def __init__(self):
        self.store = JsonStore('token_store.json')
        self.user_data = None
    
    def save_token(self, token_data):
        """Save JWT tokens to storage"""
        self.store.put('token', access=token_data['access'], refresh=token_data['refresh'])
    
    def get_token(self):
        """Get the access token"""
        if self.store.exists('token'):
            return self.store.get('token')['access']
        return None
    
    def get_refresh_token(self):
        """Get the refresh token"""
        if self.store.exists('token'):
            return self.store.get('token')['refresh']
        return None
    
    def clear_tokens(self):
        """Clear all tokens"""
        if self.store.exists('token'):
            self.store.delete('token')
    
    def save_user_data(self, user_data):
        """Save user data"""
        self.user_data = user_data
        self.store.put('user_data', **user_data)
    
    def get_user_data(self):
        """Get saved user data"""
        if self.user_data:
            return self.user_data
        
        if self.store.exists('user_data'):
            self.user_data = self.store.get('user_data')
            return self.user_data
        
        return None
    
    def get_user_role(self):
        """Get user role"""
        user_data = self.get_user_data()
        if user_data and 'role' in user_data:
            return user_data['role']
        return None