"""
session_manager.py
------------------
Intention: Manages the user's login state (Standard vs Admin) and privileges.
"""

class SessionManager:
    def __init__(self, file_handler):
        self.isLoggedIn = False
        self.isAdmin = False
        self.file_handler = file_handler

    def login(self, session_type):
        if self.isLoggedIn:
            print("Error: Already logged in.")
            return

        if session_type == 'admin':
            self.isLoggedIn = True
            self.isAdmin = True
            self.file_handler.write_transaction(f"10 {session_type} 00000 00000 **")
            print("Logged in as Admin.")
        elif session_type == 'standard':
            self.isLoggedIn = True
            self.isAdmin = False
            self.file_handler.write_transaction(f"10 {session_type} 00000 00000 **")
            print("Logged in as Standard User.")
        else:
            print("Error: Invalid login type.")

    def logout(self):
        if not self.isLoggedIn:
            print("Error: Not logged in.")
            return

        self.isLoggedIn = False
        self.isAdmin = False
        self.file_handler.write_transaction("00 00000 00000 00000 **")
        print("Session terminated.")