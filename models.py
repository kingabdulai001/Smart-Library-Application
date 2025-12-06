from db import Database
from datetime import date, timedelta

db = Database()  # Singleton instance

class Role:
    @staticmethod
    def get_role_id(role_name):
        result = db.fetchone("SELECT role_id FROM role WHERE role_name = %s", (role_name,))
        return result[0] if result else None


class User:
    @staticmethod
    def login(username, password):
        user = db.fetchone(
            "SELECT u.user_id, u.username, u.role_id FROM users u WHERE u.username=%s AND u.password=%s",
            (username, password)
        )
        return user  # (user_id, username, role_id) or None

    @staticmethod
    def username_exists(username):
        result = db.fetchone("SELECT 1 FROM users WHERE username = %s", (username,))
        return result is not None

    @staticmethod
    def email_exists(email):
        result = db.fetchone("SELECT 1 FROM member WHERE email = %s", (email,))
        return result is not None

    @staticmethod
    def register(username, password, full_name, email):
        if User.username_exists(username):
            return False, "Username already taken!"
        if User.email_exists(email):
            return False, "Email already registered!"

        try:
            # Get Member role (role_name = 'Member')
            role_row = db.fetchone("SELECT role_id FROM role WHERE role_name = 'Member'")
            if not role_row:
                return False, "Member role not found!"
            role_id = role_row[0]

            # Insert user
            db.execute(
                "INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s) RETURNING user_id",
                (username, password, role_id)
            )
            user_id = db.cur.fetchone()[0]

            # Insert member profile
            db.execute(
                "INSERT INTO member (user_id, name, email) VALUES (%s, %s, %s)",
                (user_id, full_name, email)
            )

            return True, "Registration successful!"
        except Exception as e:
            db.conn.rollback()
            return False, f"Registration failed: {str(e)}"


class Book:
    @staticmethod
    def search(title="", author=""):
        query = """
            SELECT b.book_id, b.title, a.name, b.isbn, b.copies_available 
            FROM book b 
            JOIN author a ON b.author_id = a.author_id
            WHERE b.title ILIKE %s AND a.name ILIKE %s
            ORDER BY b.title
        """
        return db.fetch(query, (f"%{title}%", f"%{author}%"))

    @staticmethod
    def borrow(book_id, member_user_id):
        # Find member_id from user_id
        member_row = db.fetchone("SELECT member_id FROM member WHERE user_id = %s", (member_user_id,))
        if not member_row:
            return False, "Member profile not found!"
        member_id = member_row[0]

        # Max 3 active loans
        active = db.fetch("SELECT COUNT(*) FROM loan WHERE member_id=%s AND return_date IS NULL", (member_id,))
        if active[0][0] >= 3:
            return False, "You can borrow max 3 books!"

        # Check availability
        copies = db.fetchone("SELECT copies_available FROM book WHERE book_id=%s", (book_id,))
        if not copies or copies[0] <= 0:
            return False, "No copies available!"

        due_date = date.today() + timedelta(days=14)  # 2 weeks

        db.execute("""
            INSERT INTO loan (book_id, member_id, due_date) 
            VALUES (%s, %s, %s)
        """, (book_id, member_id, due_date))

        db.execute("UPDATE book SET copies_available = copies_available - 1 WHERE book_id=%s", (book_id,))
        return True, f"Book borrowed! Due: {due_date}"

    @staticmethod
    def return_book(loan_id):
        loan = db.fetchone("SELECT book_id FROM loan WHERE loan_id=%s AND return_date IS NULL", (loan_id,))
        if not loan:
            return False, "Loan not found or already returned!"

        db.execute("UPDATE loan SET return_date = CURRENT_DATE WHERE loan_id=%s", (loan_id,))
        book_id = loan[0]
        db.execute("UPDATE book SET copies_available = copies_available + 1 WHERE book_id=%s", (book_id,))
        return True, "Book returned successfully!"