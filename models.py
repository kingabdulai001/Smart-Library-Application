# models.py
from db import Database
from datetime import date, timedelta

db = Database()

class Role:
    @staticmethod
    def get_role_id(role_name):
        result = db.fetchone("SELECT role_id FROM role WHERE role_name = %s", (role_name,))
        return result[0] if result else None

class User:
    @staticmethod
    def login(username, password):
        user = db.fetchone("SELECT user_id, username, role_id FROM users WHERE username=%s AND password=%s",
                           (username, password))
        return user  # (user_id, username, role_id)

class Book:
    @staticmethod
    def search(title="", author=""):
        query = """
            SELECT b.book_id, b.title, a.name, b.isbn, b.copies_available 
            FROM book b JOIN author a ON b.author_id = a.author_id
            WHERE b.title ILIKE %s AND a.name ILIKE %s
        """
        return db.fetch(query, (f"%{title}%", f"%{author}%"))

    @staticmethod
    def borrow(book_id, member_id):
        # Check max 3 loans
        active = db.fetch("SELECT COUNT(*) FROM loan WHERE member_id=%s AND return_date IS NULL", (member_id,))
        if active[0][0] >= 3:
            return False, "Maximum 3 books allowed!"

        # Check availability
        copies = db.fetchone("SELECT copies_available FROM book WHERE book_id=%s", (book_id,))
        if not copies or copies[0] <= 0:
            return False, "No copies available!"

        # Create loan
        due_date = date.today() + timedelta(days=7)
        db.execute("""
            INSERT INTO loan (book_id, member_id, due_date) 
            VALUES (%s, %s, %s)
        """, (book_id, member_id, due_date))

        db.execute("UPDATE book SET copies_available = copies_available - 1 WHERE book_id=%s", (book_id,))
        return True, "Book borrowed successfully!"

    @staticmethod
    def return_book(loan_id):
        db.execute("UPDATE loan SET return_date = CURRENT_DATE WHERE loan_id=%s", (loan_id,))
        book_id = db.fetchone("SELECT book_id FROM loan WHERE loan_id=%s", (loan_id,))[0]
        db.execute("UPDATE book SET copies_available = copies_available + 1 WHERE book_id=%s", (book_id,))
