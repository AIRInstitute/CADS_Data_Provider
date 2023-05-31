from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(UserMixin, db.Model):
    """
    User model for handling user data in the application. It inherits from UserMixin and db.Model.

    Attributes:
        id (str): The unique identifier for the user, serving as the primary key in the database.
        username (str): The username of the user. It is unique and cannot be null.
        email (str): The email of the user. It can be null.
        urn (str, optional): Optional URN field. Default is None.
        is_active (bool): A boolean flag indicating if the user is active. Default is True.
        is_authenticated (bool): A boolean flag indicating if the user is authenticated. Default is True.
    """
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    urn = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=True)

    def __init__(self, id, username, email):
        """
        The constructor for the User class.

        Parameters:
            id (str): The unique identifier for the user.
            username (str): The username of the user.
            email (str): The email of the user.
        """
        self.id = id
        self.username = username
        self.email = email
        self.is_active = True
        self.is_authenticated = True
    
    def get_id(self):
        """
        Method to get the id of the user.

        Returns:
            str: The id of the user.
        """
        return self.id
    


