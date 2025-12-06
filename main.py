# main.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models import User, Book, db

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartLibrary - Login")
        self.setGeometry(300, 300, 400, 200)

        widget = QWidget()
        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.current_user = None

    def login(self):
        username = self.username.text()
        password = self.password.text()
        user = User.login(username, password)
        if user:
            self.current_user = {"id": user[0], "username": user[1], "role_id": user[2]}
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials!")

    def open_main_window(self):
        self.main_win = MainWindow(self.current_user)
        self.main_win.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"SmartLibrary - Welcome {user['username']}")
        self.setGeometry(100, 100, 1000, 600)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()
        
        tabs.addTab(self.book_catalog_tab(), "Book Catalog")
        tabs.addTab(self.borrow_tab(), "Borrow/Return")
        tabs.addTab(self.dashboard_tab(), "Dashboard")

        self.setCentralWidget(tabs)

    def book_catalog_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        title_input = QLineEdit()
        title_input.setPlaceholderText("Search by title...")
        author_input = QLineEdit()
        author_input.setPlaceholderText("Author...")
        search_btn = QPushButton("Search")
        
        search_layout.addWidget(title_input)
        search_layout.addWidget(author_input)
        search_layout.addWidget(search_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Available"])

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        def search():
            books = Book.search(title_input.text(), author_input.text())
            self.table.setRowCount(len(books))
            for i, book in enumerate(books):
                for j, val in enumerate(book):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

        search_btn.clicked.connect(search)
        search()  # load all initially

        widget.setLayout(layout)
        return widget

    def borrow_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        book_id_input = QLineEdit()
        book_id_input.setPlaceholderText("Enter Book ID to borrow")
        borrow_btn = QPushButton("Borrow Book")
        
        return_input = QLineEdit()
        return_input.setPlaceholderText("Enter Loan ID to return")
        return_btn = QPushButton("Return Book")

        self.borrow_status = QLabel("")

        borrow_btn.clicked.connect(lambda: self.borrow_book(book_id_input.text()))
        return_btn.clicked.connect(lambda: self.return_book(return_input.text()))

        layout.addWidget(QLabel("Borrow Book"))
        layout.addWidget(book_id_input)
        layout.addWidget(borrow_btn)
        layout.addWidget(QLabel("Return Book"))
        layout.addWidget(return_input)
        layout.addWidget(return_btn)
        layout.addWidget(self.borrow_status)

        widget.setLayout(layout)
        return widget

    def borrow_book(self, book_id_str):
        if not book_id_str.isdigit():
            self.borrow_status.setText("Invalid Book ID")
            return
        success, msg = Book.borrow(int(book_id_str), self.user['id'])
        self.borrow_status.setText(msg)

    def return_book(self, loan_id_str):
        if not loan_id_str.isdigit():
            self.borrow_status.setText("Invalid Loan ID")
            return
        Book.return_book(int(loan_id_str))
        self.borrow_status.setText("Book returned!")

    def dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Welcome to SmartLibrary Dashboard!\nMore features coming soon...")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
