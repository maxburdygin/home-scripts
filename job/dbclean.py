import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('db/taskreminder.db')
cursor = conn.cursor()

# Проверяем наличие таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='taskreminder';")
table_exists = cursor.fetchone()

if table_exists:
    # Очищаем таблицу taskreminder
    cursor.execute("DELETE FROM taskreminder;")
    conn.commit()
    print("Таблица 'taskreminder' успешно очищена.")
else:
    print("Таблица 'taskreminder' не найдена.")

# Закрываем соединение с базой данных
conn.close()
