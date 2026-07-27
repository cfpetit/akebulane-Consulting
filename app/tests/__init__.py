import unittest

from app import create_app, db
from app.auth.models import User

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
            BaseTestClass.create_user('admin', 'admin@xyz.com', '1111', True)
            BaseTestClass.create_user('guest', 'guest@xyz.com', '1111', False)

    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()
    
    @staticmethod
    def create_user(name, email, password, is_admin):
        user = User(name, email)
        user.set_password(password)
        user.save()
        return user