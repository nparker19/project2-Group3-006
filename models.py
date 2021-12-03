'''
this script is define and create model
for the database used in the app
'''
import os
from flask_login import UserMixin
from app import db


# keep the class name as User_DB to avoid error despite pylint suggestion
class User_DB(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))

    def __repr__(self):
        ''' object defined
        '''
        return f"<User {self.email}>"
    
    def get_username(self):
        ''' get username defined
        '''
        return self.email


if os.getenv("DATABASE_URL") is not None:  # so our unit tests run in GitHub
    db.create_all()
