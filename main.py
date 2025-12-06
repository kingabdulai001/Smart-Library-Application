import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

from models import User, Book
from db import Database

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

        # Logo / Title
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
    # ... (same as before — Book Catalog, Borrow/Return, etc.)
    # I'll keep it short — you already have this part working
    # Just make sure it uses: self.user["id"] when borrowing
    pass  # Keep your existing MainWindow code here


# ←←←← Paste your full working MainWindow class here (the one from previous messages) ←←←←

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())