import os
import datetime
import argparse
import sqlite3

# Обработка аргументов командной строки
parser = argparse.ArgumentParser(description="Process daily tasks.")
parser.add_argument('--today', type=str, help='Date in YYYY-MM-DD format', required=False)
args = parser.parse_args()

# Задаем путь к папке с заметками
NOTES_PATH = "/Users/user/Yandex.Disk-maksim.burdygin.localized/Obsidian vault/Daily"
TEMPLATE_PATH = "/Users/user/Yandex.Disk-maksim.burdygin.localized/Obsidian vault/Templates/Daily.md"

# Вычисляем даты
if args.today:
    try:
        today = datetime.datetime.strptime(args.today, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        exit()
else:
    today = datetime.date.today()

yesterday = today - datetime.timedelta(days=1)

# Формируем имена файлов
yesterday_file = yesterday.strftime("%Y-%m-%d") + ".md"
today_file = today.strftime("%Y-%m-%d") + ".md"

# Полные пути до файлов
yesterday_path = os.path.join(NOTES_PATH, yesterday_file)
today_path = os.path.join(NOTES_PATH, today_file)

# Если файл вчерашней заметки не существует
if not os.path.exists(yesterday_path):
    print(f"Yesterday's note ({yesterday_path}) does not exist.")
    exit()

# Считываем шаблон
template_content = ""
if os.path.exists(TEMPLATE_PATH):
    with open(TEMPLATE_PATH, 'r') as template_file:
        template_content = template_file.read()
else:
    print(f"Template file ({TEMPLATE_PATH}) does not exist.")
    exit()

y_tasks = []
tasks_to_remind = []
ignore_morning = False
ignore_evening = False

# Считываем звездочки за утреннюю и вечернюю рутину
morning_stars = {}
evening_stars = {}

with open(yesterday_path, 'r') as yf:
    lines = yf.readlines()

    with open(yesterday_path, 'w') as yf:
        for line in lines:
            if line.startswith("### "):
                ignore_morning = False
                ignore_evening = False

            # Если задача со смайликом 👨🏼‍🎓, добавляем в tasks_to_remind
            if "👨🏼‍🎓" in line and (line.startswith("- [ ]") or line.startswith("- [x]")):
                print(f"line is {line}")
                tasks_to_remind.append(line)

            # если строка - задача не из утреннней или вечерней рутины, переносим ее
            if line.startswith("- [ ]") and not (ignore_morning or ignore_evening):
                y_tasks.append(line)
            elif not (ignore_morning or ignore_evening):
                yf.write(line)

            # выполненные задачи из утра или вечера - оставляем
            elif line.startswith("- [x]") and (ignore_morning or ignore_evening):
                yf.write(line)

            # этот иф внизу чтобы заголовок не удаляло
            if line.strip() == "### Morning Routine":
                ignore_morning = True
            elif line.strip() == "### Evening Routine":
                ignore_evening = True

            # считаем кол-во звезд в утренней рутине
            if line.startswith("- [x]") and ignore_morning:
                parts = line.split(" ")
                task = parts[2]
                stars = line.count("⭐️")
                morning_stars[task] = stars + 1

            # считаем кол-во звезд в вечерней рутине
            if line.startswith("- [x]") and ignore_evening:
                parts = line.split(" ")
                task = parts[2]
                stars = line.count("⭐️")
                evening_stars[task] = stars + 1

# Если файл сегодняшней заметки не существует - создаем его
if not os.path.exists(today_path):
    with open(today_path, 'a') as f:
        f.write(template_content)
        f.write("\n")

with open(today_path, 'r') as tf:
    lines = tf.readlines()

# Флаг для проверки наличия раздела "### Yesterday Tasks"
has_section = any(line.strip() == "### Yesterday Tasks" for line in lines)

# Если раздела нет - добавляем его
if not has_section:
    lines.append("### Yesterday Tasks\n")


# Подключение к SQLite и создание таблицы, если она не существует
conn = sqlite3.connect('taskreminder.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS taskreminder (
    date TEXT,
    task TEXT
)
''')

# Обработка задач со смайликом 👨🏼‍🎓
for task in tasks_to_remind:
    if task.startswith("- [ ]"):
        task = task[5:]
    elif task.startswith("- [x]"):
        task = task[5:]

    task = task.strip()

    # Удаление даты и зеленой галочки, если они есть
    if "✅" in task:
        task = task.split("✅", 1)[0].strip()  # Извлекаем текст задачи до зеленой галочки
    if "👨🏼‍🎓" in task:
        task = task.split("👨🏼‍🎓", 1)[0].strip()  # Извлекаем текст задачи до смайлика со шляпкой

    # Вставка задачи в SQLite на разные даты
    dates = [
        today,
        today + datetime.timedelta(days=1),
        today + datetime.timedelta(days=2),
        today + datetime.timedelta(days=7),
        today + datetime.timedelta(days=14),
        today + datetime.timedelta(days=30)
    ]
    print(f"date {dates}, task is {task}")
    for date in dates:
        cursor.execute('INSERT INTO taskreminder (date, task) VALUES (?, ?)', (date.strftime("%Y-%m-%d"), task))

# Добавляем задачи в конец файла и в SQLite
with open(today_path, 'w') as tf:
    for line in lines:
        if line.startswith("- [ ]"):
            parts = line.split(" ")
            task = parts[3].strip()
            # Добавляем звездочки к утренней рутине (которая уже в шаблоне)
            if task in morning_stars:
                stars = "⭐️" * morning_stars[task]
                new_line = f"- [ ] {task} {stars}\n"
                tf.write(new_line)
            elif task in evening_stars:
                stars = "⭐️" * evening_stars[task]
                new_line = f"- [ ] {task} {stars}\n"
                tf.write(new_line)
            else:
                tf.write(line)
        else:
            tf.write(line)
    for task in y_tasks:
        tf.write(task)

    # Выбираем задачи за сегодняшний день из таблицы
    cursor.execute("SELECT task FROM taskreminder WHERE date = ?", (today,))
    tasks_from_db = cursor.fetchall()
    print(f"Tasks from db {tasks_from_db}, today is {today}")
    # Добавляем задачи из таблицы в список y_tasks
    for task in tasks_from_db:
        tf.write(f"- [ ] {task[0]}\n")
        # Удаляем задачу из таблицы taskreminder по её идентификатору
        cursor.execute("DELETE FROM taskreminder WHERE task = ? and date = ?", (task[0], str(today)))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
