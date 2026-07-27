# config/testing.py

from .default import *
from sqlalchemy.pool import NullPool

# Disable pooling during tests to prevent PostgreSQL transaction deadlocks
SQLALCHEMY_ENGINE_OPTIONS = {
    "poolclass": NullPool
}


# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING

WTF_CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'
