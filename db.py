# database.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            
            
            url = os.getenv("NEON_DB_URL")
            if not url:
                raise Exception("Set NEON_DB_URL in your .env file!")
                
            # This extra parameter is needed for Neon's certificate
            cls._instance.conn = psycopg2.connect(
                url,
                sslmode="require"   # <-- Important for Neon
            )
            cls._instance.cur = cls._instance.conn.cursor()
        return cls._instance

    def execute(self, query, params=None):
        self.cur.execute(query, params or ())
        self.conn.commit()

    def fetch(self, query, params=None):
        self.cur.execute(query, params or ())
        return self.cur.fetchall()

    def fetchone(self, query, params=None):
        self.cur.execute(query, params or ())
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()
        

# # database.py
# import psycopg2
# from urllib.parse import urlparse

# class Database:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Database, cls).__new__(cls)
#             # === PUT YOUR SUPABASE URL HERE ===
#             supabase_url = "postgresql://postgres:lexluth0r@db.dmoqebocifxbnvdfgjhc.supabase.co:5432/postgres"

#             cls._instance.conn = psycopg2.connect(supabase_url)
#             cls._instance.cur = cls._instance.conn.cursor()
#         return cls._instance

#     @classmethod
#     def get_instance(cls):
#         return cls()

#     def execute(self, query, params=None):
#         self.cur.execute(query, params or ())
#         self.conn.commit()

#     def fetch(self, query, params=None):
#         self.cur.execute(query, params or ())
#         return self.cur.fetchall()

#     def fetchone(self, query, params=None):
#         self.cur.execute(query, params or ())
#         return self.cur.fetchone()

#     def close(self):
#         self.cur.close()
#         self.conn.close()
