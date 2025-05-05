import unittest
from unittest.mock import patch, MagicMock
import bcrypt
import sys
import os

# Ajustar path para importar módulos de email_sender_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'email_sender_app')))

from . import register
from . import app

class TestUserAuth(unittest.TestCase):

    @patch('register.connect_db')
    def test_register_user_success(self, mock_connect_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        # Simular que no hay error en la inserción
        mock_cursor.execute.return_value = None
        mock_db.commit.return_value = None

        # Llamar a la función register_user con datos válidos
        register.register_user('testuser', 'test@example.com', 'Password1', 'Password1', MagicMock())

        # Verificar que se haya llamado a execute con los parámetros correctos
        self.assertTrue(mock_cursor.execute.called)
        args, kwargs = mock_cursor.execute.call_args
        self.assertIn('INSERT INTO users', args[0])
        self.assertEqual(args[1][0], 'testuser')
        self.assertEqual(args[1][1], 'test@example.com')

    @patch('app.connect_db')
    def test_login_user_success(self, mock_connect_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        # Crear hash de contraseña para comparar
        password = 'Password1'
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Simular fetchone para devolver usuario con hash
        mock_cursor.fetchone.return_value = (1, hashed)

        # Simular messagebox para evitar GUI popups
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = app.login_user('testuser', password, MagicMock())
            self.assertTrue(result)
            mock_info.assert_called_with("Éxito", "Inicio de sesión exitoso")

    @patch('app.connect_db')
    def test_login_user_wrong_password(self, mock_connect_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        # Contraseña incorrecta
        password = 'WrongPass'
        hashed = bcrypt.hashpw('Password1'.encode('utf-8'), bcrypt.gensalt())

        mock_cursor.fetchone.return_value = (1, hashed)

        with patch('tkinter.messagebox.showerror') as mock_error:
            result = app.login_user('testuser', password, MagicMock())
            self.assertFalse(result)
            mock_error.assert_called_with("Error", "Contraseña incorrecta")

if __name__ == '__main__':
    unittest.main()
