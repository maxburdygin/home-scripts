import sqlite3
import os

# Получение текущей директории
# current_directory = os.getcwd()

# Получение списка файлов в текущей директории
# files = os.listdir(current_directory)
# print(files)


# Путь к базе данных
# db_path = 'taskreminder.db'

# Проверка, существует ли файл базы данных
# if os.path.exists(db_path):
#     print("Database exists.")
# else:
#     print("Database does not exist.")

# Подключаемся к базе данных
conn = sqlite3.connect('/Users/user/IdeaProjects/home-pets/job/db/budget.db')

# Создаем курсор
cursor = conn.cursor()

# Выполняем запрос для получения списка таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Получаем результаты
tables = cursor.fetchall()

# Печатаем список таблиц
print("Tables in the database:")
for table in tables:
    print(table[0])

# Извлекаем данные из таблицы
cursor.execute("SELECT * FROM asset")
rows = cursor.fetchall()

if rows:
    print("Данные в таблице 'asset':")
    for row in rows:
        print(row)
else:
    print("Таблица 'asset' пуста.")
    print("Таблица 'asset' пуста.")

# Закрываем соединение с базой данных
conn.close()
