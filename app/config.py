import os

SECRET_KEY = ''

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
ADMIN_ROLE_ID = 1
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')