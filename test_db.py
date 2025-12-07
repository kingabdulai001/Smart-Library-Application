import unittest
from unittest.mock import patch, MagicMock
from db import Database

class TestDatabase(unittest.TestCase):

    @patch('db.psycopg2.connect')
    def test_database_connection(self, mock_connect):
        # Mock the connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db = Database()
        self.assertIsNotNone(db.conn)
        mock_connect.assert_called_once()

    @patch('db.Database.execute')
    def test_execute_query(self, mock_execute):
        # Mock execute method
        db = Database()
        db.execute("SELECT * FROM users")
        mock_execute.assert_called_once_with("SELECT * FROM users")

    @patch('db.Database.fetch')
    def test_fetch_query(self, mock_fetch):
        # Mock fetch method
        mock_fetch.return_value = [(1, 'testuser')]

        db = Database()
        result = db.fetch("SELECT * FROM users")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'testuser')
        mock_fetch.assert_called_once_with("SELECT * FROM users")

if __name__ == '__main__':
    unittest.main()