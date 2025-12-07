import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from main import LoginWindow, MainWindow

class TestMain(unittest.TestCase):

    @patch('main.User.login')
    def test_login_success(self, mock_login):
        # Mock login response
        mock_login.return_value = (1, 'testuser', 2)

        app = QApplication([])
        login_window = LoginWindow()
        login_window.username.setText('testuser')
        login_window.password.setText('password')
        
        login_window.login()
        mock_login.assert_called_once_with('testuser', 'password')

    @patch('main.User.login')
    def test_login_failure(self, mock_login):
        # Mock login failure
        mock_login.return_value = None

        app = QApplication([])
        login_window = LoginWindow()
        login_window.username.setText('wronguser')
        login_window.password.setText('wrongpass')
        
        login_window.login()
        mock_login.assert_called_once_with('wronguser', 'wrongpass')

if __name__ == '__main__':
    unittest.main()