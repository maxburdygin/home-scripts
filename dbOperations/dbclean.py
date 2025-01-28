import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('/Users/user/IdeaProjects/home-pets/job/db/budget.db')
cursor = conn.cursor()

# Проверяем наличие таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='asset';")
table_exists = cursor.fetchone()

if table_exists:
    # Очищаем таблицу asset
    cursor.execute("DELETE FROM asset;")
    conn.commit()
    print("Таблица 'asset' успешно очищена.")
else:
    print("Таблица 'asset' не найдена.")

# Закрываем соединение с базой данных
conn.close()
