accounts = []

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def add_account(self):
        new_user = dict(
            username = self.username,
            email = self.email,
            password = self.password
        )
        if any(user["username"] == self.username for user in accounts):
            return False
        accounts.append(new_user)
        return True
    
    @staticmethod
    def login(username, password):
        _username = username
        _password = password

        if any(user["username"] == _username for user in accounts):
            if any(passwrd["password"] == _password for passwrd in accounts):
                return True
            return False
        return False

    # @staticmethod
    # def change_password(username, old_password, new_password):
    #     for account in range(len(accounts)):
    #         if accounts[account]["username"] == username:
    #             if accounts[account]["password"] == old_password:
    #                 accounts[account]["password"] = new_password
    #                 return True
    #             return False
    #         return False

    # @staticmethod
    # def change_email(username, password, new_email):
    #     for account in range(len(accounts)):
    #         if accounts[account]["username"] == username:
    #             if accounts[account]["password"] == password:
    #                 accounts[account]["email"] = new_email
    #                 return True
    #             return False
    #         return False

    @staticmethod
    def delete_account(username, password):
        for account in range(len(accounts)):
            if accounts[account]["username"] == username:
                if accounts[account]["password"] == password:
                    del accounts[account]
                    return True
                return False
        return False
          



                