class sessionManager:
    isLoggedIn = False
    isAdmin = False


    def __init__(self):
        self.isLoggedIn = False
        self.isAdmin = False
    
    def login(self):
        self.isLoggedIn = True
    def logout(self):
        self.isLoggedIn = False