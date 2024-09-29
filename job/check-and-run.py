import os
import datetime
import subprocess

from constants import LAST_PROCESSED_FILE_PATH, MOVER_SCRIPT_PATH

# Путь к файлу, в котором хранится дата последнего запуска
LAST_PROCESSED_FILE = LAST_PROCESSED_FILE_PATH
MOVER_SCRIPT = MOVER_SCRIPT_PATH

def get_last_processed_date():
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, 'r') as file:
            date_str = file.read().strip()
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
    return None

def update_last_processed_date(date_to_write):
    with open(LAST_PROCESSED_FILE, 'w') as file:
        file.write(date_to_write)

def main():
    last_processed_date = get_last_processed_date()
    today_processing = last_processed_date + datetime.timedelta(days=1)
    today = datetime.date.today()
    print(f"Started at {datetime.datetime.now()}, Today is {today}, Last processed {last_processed_date}, next {today_processing}")

    if last_processed_date == today:
        print("Already processed for today.")
        return

    # Запуск основного скрипта
    subprocess.run(["python3", MOVER_SCRIPT, "--today", today_processing.strftime("%Y-%m-%d")])
    # Обновление даты последней обработки
    update_last_processed_date(today_processing.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    main()
