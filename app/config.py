import os

# SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
ADMIN_ROLE_ID = 1
MODERATOR_ROLE_ID = 2
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')