# config/default.py

from os.path import abspath, dirname
import os


# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

#Configuración del Email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'cfranciapetit@gmail.com'
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
DONT_REPLY_FROM_EMAIL = 'cfranciapetit@gmail.com'
ADMINS = ('cfranciapetit@gmail.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False
