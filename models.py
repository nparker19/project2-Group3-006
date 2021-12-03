'''
this script is define and create model
for the database used  in the app
'''
import os
from flask_login import UserMixin
from app import db

# disabled pylint
# models.py:11:0: C0103: Class name "User_DB" doesn't conform to PascalCase naming style (invalid-name)
# models.py:15:9: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
# models.py:15:19: E1101: Instance of 'SQLAlchemy' has no 'Integer' member (no-member)
# models.py:16:12: E1101: Instance of 'SQLAlchemy' has no 'Column' member (no-member)
# models.py:16:22: E1101: Instance of 'SQLAlchemy' has no 'String' member (no-member)
# keep the class name as User_DB to avoid error despite pylint suggestion
class User_DB(UserMixin, db.Model):
    """
    database class defined
    """
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
