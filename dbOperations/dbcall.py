import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('/Users/user/taskreminder.db')
# conn = sqlite3.connect('/Users/user/IdeaProjects/home-pets/job/db/budget.db')

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


# Подключаемся к базе данных
conn = sqlite3.connect('/Users/user/taskreminder.db')
# conn = sqlite3.connect('/Users/user/IdeaProjects/home-pets/job/db/budget.db')
cursor = conn.cursor()

# Проверяем наличие таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='taskreminder';")
table_exists = cursor.fetchone()

if table_exists:
    print("Таблица 'taskreminder' существует.")

    # Извлекаем данные из таблицы
    cursor.execute("SELECT * FROM taskreminder;")
    rows = cursor.fetchall()

    if rows:
        print("Данные в таблице 'taskreminder':")
        for row in rows:
            print(row)
    else:
        print("Таблица 'taskreminder' пуста.")
else:
    print("Таблица 'taskreminder' не найдена.")

# Закрываем соединение с базой данных
conn.close()
