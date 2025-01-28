import sys
import os
import datetime
import subprocess

# Добавляем корневую директорию в путь поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.budgetassetsfinder import find_budget_notes, extract_and_format_date
from util.constants import MOVER_SCRIPT_PATH, LAST_DAILY_UPDATE, LAST_BUDGET_NOTE_DATE, BASE_NOTES_PATH
from util.utils import read_param_from_config, update_param_in_config

# Путь к файлу, в котором хранится дата последнего запуска
LAST_PROCESSED_DATE = read_param_from_config(LAST_DAILY_UPDATE)
MOVER_SCRIPT = MOVER_SCRIPT_PATH

# Определяем дату создания последней бюджетной заметки в конфиг файле
LAST_BUDGET_DATE = read_param_from_config(LAST_BUDGET_NOTE_DATE)

def daily_note_processor():
    last_processed_date = datetime.datetime.strptime(LAST_PROCESSED_DATE, "%Y-%m-%d").date()
    today_processing = last_processed_date + datetime.timedelta(days=1)
    today = datetime.date.today()
    today_str = today_processing.strftime("%Y-%m-%d")
    print(f"Started at {datetime.datetime.now()}, Today is {today_str}, Last processed {last_processed_date}, next {today_processing}")

    if last_processed_date == today:
        print("Already processed for today.")
        return

    # Запуск основного скрипта
    subprocess.run(["python3", MOVER_SCRIPT, "--today", today_str])
    # Обновление даты последней обработки
    update_param_in_config(LAST_DAILY_UPDATE, today_str)

def budget_processor():
    last_processed_date = datetime.datetime.strptime(LAST_BUDGET_DATE, "%Y-%m-%d").date()
    # Кол-во дней гэпа между бюджетными заметками
    next_proposed_date = last_processed_date + datetime.timedelta(days=14)
    today = datetime.date.today()
    print(f"Last budget note was on {last_processed_date}, Today is {today}, next note to be {next_proposed_date}")

    # Получение последней даты заметки
    budget_notes = find_budget_notes(BASE_NOTES_PATH)
    if budget_notes:
        latest_note = max(budget_notes)
        print(f"max note is {latest_note}")
        formatted_date = extract_and_format_date(latest_note)
        form_date = datetime.datetime.strptime(formatted_date, "%Y-%m-%d").date()
        if (form_date >= last_processed_date):
            update_param_in_config('LAST_BUDGET_NOTE_DATE', formatted_date)
            print(f"Последняя Заметка с бюджетом обновлена на - {formatted_date}")
    else:
        print("Заметки с бюджетом не найдены.")

    # 1 - смотрим в бюджетные заметки, определяем последнюю, если дата не совпадает с конфигом переписываем конфиг

    # 2 - если работает триггер на создание бюджетной заметки то вписываем ее в текущие таски daily note

    # 3 - создаем бюджетную заметку, скопировав таблицу и основные разделы,
    #     делаем ссылку на предыдущую заметку, в предыдущей заметке - ссылку на следующую

    # 4 - добавляем или обновляем граффик


if __name__ == "__main__":
    daily_note_processor()
    budget_processor()
