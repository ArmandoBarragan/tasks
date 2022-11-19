import os
from sqlalchemy.ext.declarative import declarative_base


# Server settings
HOST = os.getenv('HOST', default='0.0.0.0')
PORT = os.getenv('PORT', default=8000)
DEBUG = os.getenv('DEBUG', default=False)


Base = declarative_base()


# Database settings
DATABASE = {
    'HOST': os.getenv('DB_HOST', default='db'),
    'PORT': os.getenv('DB_PORT', default=5432),
    'PASSWORD': os.getenv('DB_PASSWORD', default='postgres'),
    'USER': os.getenv('DB_USER', default='postgres'),
    'NAME': os.getenv('DB_NAME', default='tasks')
}