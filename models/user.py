from models.base_model import BaseModel
# from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import peewee as pw


class User(UserMixin, BaseModel):
    name = pw.CharField(unique=True)
    password = pw.CharField()
    email = pw.CharField(unique=True)
    profile_picture = pw.TextField(null = True)
    # role = pw.CharField(default="user")

    def validate(self):
        duplicate_name = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)
        # same_name = User.get_or_none(User.name!= self.name)
        if duplicate_name:
            self.errors.append('Username has already been taken!')
            # print(self.name)
            # print(duplicate_name.name)
        if duplicate_email:
            self.errors.append('Email has already been signed up!')
            # print('testing2')
        # if same_name:
            # self.errors.append('Loggin Failed! Please try agian.')
        # if len(self.password) < 8 :
        #     self.errors.append('Password must not less than 8 characters')
        # if len(self.password) > 25:
        #     self.errors.append('Password must not more than 25 characters')
        # else:
        #     self.password=generate_password_hash(self.password)

    def is_authenticated():
        return True

