import sqlite3
import os

# Проверяем, существует ли файл
db_file = "test.db"
if not os.path.exists(db_file):
    print(f"❌ Файл {db_file} не существует!")
    exit()

# Подключаемся и смотрим таблицы
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"✅ Файл {db_file} существует")
print(f"📋 Таблицы в базе данных:")
if tables:
    for table in tables:
        print(f"   - {table[0]}")
else:
    print("   (нет таблиц)")

conn.close()
