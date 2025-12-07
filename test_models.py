import unittest
from unittest.mock import patch, MagicMock
from models import User, Book, Member, Dashboard

class TestModels(unittest.TestCase):

    @patch('models.db')
    def test_user_login(self, mock_db):
        # Mock database response
        mock_db.fetchone.return_value = (1, 'testuser', 2)

        result = User.login('dominicOT', 'mechanicus')
        self.assertEqual(result, (1, 'testuser', 2))
        mock_db.fetchone.assert_called_once_with(
            "SELECT u.user_id, u.username, u.role_id FROM users u WHERE u.username=%s AND u.password=%s",
            ('dominicOT', 'mechanicus')
        )

    @patch('models.db')
    def test_book_search(self, mock_db):
        # Mock database response
        mock_db.fetch.return_value = [
            (1, 'Book Title', 'Author Name', '1234567890', 5)
        ]

        result = Book.search(title='Book', author='Author')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Book Title')
        mock_db.fetch.assert_called_once()

    @patch('models.db')
    def test_member_ban(self, mock_db):
        # Mock database execution
        mock_db.execute.return_value = None

        success, msg = Member.ban_member(1)
        self.assertTrue(success)
        self.assertEqual(msg, "Member banned successfully.")
        mock_db.execute.assert_called_once_with(
            "UPDATE member SET banned = TRUE WHERE member_id = %s", (1,)
        )

    @patch('models.db')
    def test_dashboard_summary(self, mock_db):
        # Mock database responses
        mock_db.fetchone.side_effect = [
            (100,),  # Total books
            (50,),   # Total borrowed books
            (200,),  # Total members
            (10,)    # Total clubs
        ]

        summary = Dashboard.get_summary()
        self.assertEqual(summary['total_books'], 100)
        self.assertEqual(summary['total_borrowed_books'], 50)
        self.assertEqual(summary['total_members'], 200)
        self.assertEqual(summary['total_clubs'], 10)
        self.assertEqual(mock_db.fetchone.call_count, 4)

if __name__ == '__main__':
    unittest.main()