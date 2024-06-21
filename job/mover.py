import os
import datetime

# Задаем путь к папке с заметками
NOTES_PATH = "/Users/user/Yandex.Disk-maksim.burdygin.localized/Obsidian vault/Daily"

# Вычисляем даты
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


y_tasks = []
with open(yesterday_path, 'r') as yf:
    lines = yf.readlines()

    with open(yesterday_path, 'w') as yf:
        for line in lines:
            # если строка - задача, переносим ее
            if line.startswith("- [ ]"):
                y_tasks.append(line)
            else:  # в противном случае оставляем в файле
                yf.write(line)

# Если файл сегодняшней заметки не существует - создаем его
if not os.path.exists(today_path):
    with open(today_path, 'a') as f:
        f.write("\n")

with open(today_path, 'r') as tf:
    lines = tf.readlines()

# Флаг для проверки наличия раздела "### Yesterday Tasks"
has_section = any(line.strip() == "### Yesterday Tasks" for line in lines)

# Если раздела нет - добавляем его
if not has_section:
    lines.append("### Yesterday Tasks\n")

# Добавляем задачи в конец файла
with open(today_path, 'w') as tf:
    for line in lines:
        tf.write(line)
    for task in y_tasks:
        tf.write(task)