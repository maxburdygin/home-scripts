import os
import sys
import re
import sqlite3
import datetime

# Добавляем корневую директорию в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.constants import BASE_NOTES_PATH, BUDGET_DB_PATH

# Путь к директории с заметками
notes_dir = BASE_NOTES_PATH

# Шаблон для поиска заметок вида "YYYYMMDD Бюджет"
note_pattern = re.compile(r'\d{8} Бюджет')

# Поиск всех заметок с нужным форматом имени
def find_budget_notes(directory):
    budget_notes = []
    for filename in os.listdir(directory):
        if note_pattern.match(filename):
            budget_notes.append(os.path.join(directory, filename))
    return budget_notes

def extract_and_format_date(file_path):
    # Извлечение имени файла из полного пути
    filename = file_path.split('/')[-1]

    # Извлечение даты из имени файла
    date_str = filename.split()[0]

    # Преобразование строки в объект datetime
    date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")

    # Преобразование объекта datetime в строку с нужным форматом
    formatted_date = date_obj.strftime("%Y-%m-%d")

    return formatted_date


# Функция для извлечения данных из заметки
def extract_asset_data(note_path):
    with open(note_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Поиск строк с суммой активов
    total_assets_eur = None
    total_assets_usd = None
    for line in lines:
        if "Total Assets" in line:
            parts = line.split('|')
            total_assets_eur = parts[3].strip().split(' ')[0]  # Например, 20200 €
        if "1€ =" in line:
            parts = line.split('|')
            total_assets_usd = parts[3].strip().split(' ')[0]  # Например, 22600 $

    # Извлечение даты из названия файла
    filename = os.path.basename(note_path)
    date_str = filename.split(' ')[0]  # Первая часть названия - это дата

    return date_str, total_assets_eur, total_assets_usd


# Функция для записи данных в базу данных
def save_to_db(db_path, date_str, eur_amount, usd_amount):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO asset (date, amount_eur, amount_usd) VALUES (?, ?, ?)",
                   (date_str, float(eur_amount.split()[0]), float(usd_amount.split()[0])))

    conn.commit()
    conn.close()


# Пример использования
budget_notes = find_budget_notes(notes_dir)
print(budget_notes)

# Основная логика
db_path = BUDGET_DB_PATH

for note_path in budget_notes:
    date_str, eur_amount, usd_amount = extract_asset_data(note_path)
    if eur_amount and usd_amount:
        save_to_db(db_path, date_str, eur_amount, usd_amount)
        print(f"Данные сохранены: {date_str}, {eur_amount}, {usd_amount}")
