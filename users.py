from werkzeug.security import generate_password_hash, check_password_hash

# Simple user storage (replace with database in production)
users = {}

class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.username

def register_user(username, password):
    if username in users:
        return False
    users[username] = generate_password_hash(password)
    return True

def validate_user(username, password):
    if username not in users:
        return False
    return check_password_hash(users[username], password) 