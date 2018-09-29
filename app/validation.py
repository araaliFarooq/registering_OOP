import re

class Validation:

    @staticmethod
    def auth_validation(user_name, email, password):
        if not user_name:
            return "username is missing"
        if user_name == " ":
            return "username is missing"
        if not re.match(r"^\S(.*\S)?$", user_name):
            return "username must have no white spaces"
        if not re.match(r"^\S(.*\S)?$", email):
            return "email must have no white spaces"    
        if len(user_name) < 4:
            return "username should be more than 4 characters long"
        if not email:
            return "email is missing"
        if email == " ":
            return "email is missing"
        if re.match("[^@]+@[^@]+\.[^@]+", email) == None:
            return "bad email format supplied"    
        if not password:
            return "password is missing"
        if re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*+])[a-zA-Z\d!@#$%^&*+]{6,10}$", password) == None:
            return "password should contain A capital letter, a small letter, a digit and a special character"    

    @staticmethod
    def login_validation(user_name, password):
        if not user_name:
            return "username is missing"
        if not password:
            return "password is missing"
    
    @staticmethod
    def validate_task(title):
        if not title:
            return "No title was given"
        if title == "  ":
            return "No title was given"
        if not re.match(r"^\S(.*\S)?$", title):
            return "title must have no white spaces" 
    
    @staticmethod
    def validate_input_type(input):
        try:
           _input = int(input)
        except ValueError:
            return "Input should be an interger"         