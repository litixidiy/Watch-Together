from werkzeug.security import check_password_hash
import flask_login
class User(flask_login.UserMixin):
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    #No application of anonymous users
    @property
    def is_anonymous(self):
        return False

    #check the password hash with the password
    def check_pw(self,password_input):
        return check_password_hash(self.password,password_input)

    #return the id
    def get_id(self):
        return self.username