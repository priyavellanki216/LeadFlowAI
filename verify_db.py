
import sqlite3
from database.db import DB_PATH

connection = sqlite3.connect(DB_PATH)

print("Database location:", DB_PATH)

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("\nDatabase tables:")

for table in tables:
    print("-", table[0])

connection.close()
