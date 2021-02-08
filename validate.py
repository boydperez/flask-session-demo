import re

class Validate:
    """
    Validate class.
    """
    username_validator = {
        'min_length': 4,
        'max_length': 15,
        'username_regex': "^[A-Za-z_][A-Za-z0-9_]*",
    }

    password_validator = {
        'min_length': 4
    }

    def set_username_validators(self, **kwargs):
        for name, value in kwargs.items():
            self.username_validator[name] = value

    def validate_username(self, username):
        if not len(username):
            return 'USERNAME_NULL' 
        if not (self.username_validator['min_length'] <= len(username) <= self.username_validator['max_length']):
            return 'USERNAME_LENGTH_VIOLATED' 
        if not (bool(re.match(self.username_validator['username_regex'], username))):
            return 'USERNAME_VIOLATED' 
        return 'PASS'

    def validate_password(self, password, confirm_password):
        if password != confirm_password:
            return 'PASSWD_UNMATCH' 
        if len(password) < self.password_validator['min_length']:
            return 'PASSWD_WEAK'
        return 'PASS' 


if __name__ == '__main__':
    test_username = '_someusername78'

    val = Validate()
    val.set_username_validators(min_length=10, max_length=20)
    print(val.validate_username(test_username.strip()))