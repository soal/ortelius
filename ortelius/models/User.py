from ortelius import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model):
    __tablename__ = 'users'

    # def __init__(self):
    #     pass

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = db.Column(db.Unicode(50), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # User email information
    email = db.Column(db.Unicode(255), nullable=False, server_default='', unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    first_name = db.Column(db.Unicode(50), nullable=True, server_default='')
    last_name = db.Column(db.Unicode(50), nullable=True, server_default='')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def is_active(self):
        return self.active


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default='', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default='')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
