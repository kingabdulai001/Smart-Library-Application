from db import Database
db = Database()
print("Connected to Neon!")
print(db.fetch("SELECT title, copies_available FROM book LIMIT 5"))