# main.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from models import User, Book, BookClub
from db import Database  # Make sure your file is named db.py

db = Database()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartLibrary - Login")
        self.setGeometry(300, 200, 420, 500)
        self.setStyleSheet("background-color: #f8f9fa;")

        central = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("SmartLibrary")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet(self.input_style())

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.input_style())

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(self.btn_style("#3498db"))
        login_btn.clicked.connect(self.login)

        register_link = QLabel('New here? <a href="#" style="color:#3498db; text-decoration:none;">Create an account</a>')
        register_link.setAlignment(Qt.AlignCenter)
        register_link.linkActivated.connect(self.open_register)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(register_link)
        layout.addStretch()

        central.setLayout(layout)
        self.setCentralWidget(central)

    def input_style(self):
        return "padding: 14px; border: 2px solid #ddd; border-radius: 10px; font-size: 16px;"

    def btn_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 14px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {self.darken(color)}; }}
        """

    def darken(self, color):
        return "#2980b9" if color == "#3498db" else "#27ae60"

    def login(self):
        user = User.login(self.username.text().strip(), self.password.text())
        if user:
            main_win = MainWindow({
                "id": user[0],
                "username": user[1],
                "role_id": user[2]
            })
            main_win.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password!")

    def open_register(self):
        self.register_win = RegisterWindow()
        self.register_win.show()
        self.close()


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartLibrary - Register")
        self.setGeometry(300, 100, 480, 680)
        self.setStyleSheet("background-color: #f8f9fa;")

        central = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)

        QLabel("Create Your Account", font=QFont("Arial", 26, QFont.Bold),
               alignment=Qt.AlignCenter, parent=central).setStyleSheet("color: #2c3e50;")
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Choose username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Create password (min 6 chars)")
        self.password.setEchoMode(QLineEdit.Password)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name")
        self.email = QLineEdit()
        self.email.setPlaceholderText("your@email.com")

        for widget in (self.username, self.password, self.name, self.email):
            widget.setStyleSheet("padding: 14px; border: 2px solid #ddd; border-radius: 10px; font-size: 15px;")
            layout.addWidget(widget)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        reg_btn = QPushButton("Register Now")
        reg_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: bold;")
        reg_btn.clicked.connect(self.register)
        layout.addWidget(reg_btn)

        login_link = QLabel('Already have an account? <a href="#" style="color:#3498db;">Login here</a>')
        login_link.setAlignment(Qt.AlignCenter)
        login_link.linkActivated.connect(self.go_login)
        layout.addWidget(login_link)
        layout.addStretch()

        central.setLayout(layout)
        self.setCentralWidget(central)

    def register(self):
        u = self.username.text().strip()
        p = self.password.text()
        n = self.name.text().strip()
        e = self.email.text().strip().lower()

        if not all([u, p, n, e]):
            return self.show_status("All fields are required!", "red")
        if len(p) < 6:
            return self.show_status("Password too short!", "red")
        if "@" not in e:
            return self.show_status("Invalid email!", "red")

        success, msg = User.register(u, p, n, e)
        self.show_status(msg, "green" if success else "red")

        if success:
            QMessageBox.information(self, "Welcome!", "Account created! Logging you in...")
            user = User.login(u, p)
            main_win = MainWindow({"id": user[0], "username": user[1], "role_id": user[2]})
            main_win.show()
            self.close()

    def show_status(self, text, color):
        self.status.setText(text)
        self.status.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 15px;")

    def go_login(self):
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"SmartLibrary - Welcome {user['username']}")
        self.setGeometry(100, 100, 1100, 700)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabBar::tab { height: 40px; width: 160px; font-size: 14px; }")

        tabs.addTab(self.book_catalog_tab(), "Book Catalog")
        tabs.addTab(self.borrow_tab(), "Borrow/Return")
        tabs.addTab(self.book_clubs_tab(), "Book Clubs")
        tabs.addTab(self.dashboard_tab(), "Dashboard")

        self.setCentralWidget(tabs)

    # ———————————————————— YOUR EXISTING TABS (keep them) ————————————————————
    def book_catalog_tab(self):
        # ← Your working book catalog code here
        pass  # Replace with your actual code

    def borrow_tab(self):
        # ← Your working borrow/return code here
        pass  # Replace with your actual code

    def dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Welcome to SmartLibrary Dashboard!\nMore features coming soon...")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    # ———————————————— BOOK CLUBS TAB (NEW) ————————————————
    def book_clubs_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Librarian: Create club
        if self.user["role_id"] == 1:
            box = QGroupBox("Create New Book Club")
            hbox = QHBoxLayout()
            name_in = QLineEdit()
            name_in.setPlaceholderText("Club Name")
            desc_in = QLineEdit()
            desc_in.setPlaceholderText("Description")
            create_btn = QPushButton("Create Club")
            create_btn.setStyleSheet("background:#27ae60;color:white;padding:10px;border-radius:8px;font-weight:bold;")

            def create():
                if name_in.text().strip():
                    success, _ = BookClub.create(name_in.text().strip(), desc_in.text().strip() or "No description", self.user["id"])
                    QMessageBox.information(self, "Success", "Club created!" if success else "Error")
                    name_in.clear()
                    desc_in.clear()
                    self.refresh_clubs()

            create_btn.clicked.connect(create)
            hbox.addWidget(name_in)
            hbox.addWidget(desc_in)
            hbox.addWidget(create_btn)
            box.setLayout(hbox)
            layout.addWidget(box)

        self.clubs_table = QTableWidget()
        self.clubs_table.setColumnCount(4)
        self.clubs_table.setHorizontalHeaderLabels(["Club Name", "Description", "Members", "Action"])
        self.clubs_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(QLabel("<h2>Book Clubs</h2>"))
        layout.addWidget(self.clubs_table)
        widget.setLayout(layout)

        self.refresh_clubs()
        return widget

    def refresh_clubs(self):
        clubs = BookClub.get_all()
        self.clubs_table.setRowCount(len(clubs))

        for i, (club_id, name, desc, count) in enumerate(clubs):
            self.clubs_table.setItem(i, 0, QTableWidgetItem(name))
            self.clubs_table.setItem(i, 1, QTableWidgetItem(desc or "—"))
            self.clubs_table.setItem(i, 2, QTableWidgetItem(str(count)))

            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.setContentsMargins(5, 5, 5, 5)

            if self.user["role_id"] == 2:  # Member
                member_row = db.fetchone("SELECT member_id FROM member WHERE user_id=%s", (self.user["id"],))
                member_id = member_row[0] if member_row else None
                joined = member_id and db.fetchone("SELECT 1 FROM club_member WHERE club_id=%s AND member_id=%s", (club_id, member_id))

                btn = QPushButton("Leave" if joined else "Join")
                btn.setStyleSheet(f"background:#{'e74c3c' if joined else '27ae60'};color:white;padding:8px;border-radius:6px;")
                def handler(cid=club_id):
                    if joined:
                        BookClub.leave(cid, self.user["id"])
                    else:
                        BookClub.join(cid, self.user["id"])
                    self.refresh_clubs()
                btn.clicked.connect(handler)
                hbox.addWidget(btn)

            view_btn = QPushButton("View Members")
            view_btn.clicked.connect(lambda _, cid=club_id, n=name: self.show_club_members(cid, n))
            hbox.addWidget(view_btn)

            self.clubs_table.setCellWidget(i, 3, widget)

        self.clubs_table.resizeColumnsToContents()

    def show_club_members(self, club_id, club_name):
        members = BookClub.get_members(club_id)
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Members - {club_name}")
        dialog.resize(500, 400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"<h3>{club_name}</h3><b>Members: {len(members)}</b>"))
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Name", "Email"])
        table.setRowCount(len(members))
        for i, (name, email) in enumerate(members):
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(email or "—"))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())