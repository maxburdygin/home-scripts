import sqlite3
from datetime import datetime, timedelta

# Шаг 1: Подключение к базе данных и извлечение данных за последний год
def fetch_recent_assets():
    conn = sqlite3.connect('/Users/user/IdeaProjects/home-pets/job/db/budget.db')
    cursor = conn.cursor()
    query = '''
    SELECT date, amount_eur, amount_usd
    FROM asset
    WHERE date >= ?;
    '''
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    cursor.execute(query, (one_year_ago,))
    data = cursor.fetchall()
    conn.close()
    return data

# Шаг 2: Преобразование строк с датами в datetime и сортировка по дате
def process_dates(data):
    processed_data = []
    for row in data:
        date_str, amount_eur, amount_usd = row
        date = datetime.strptime(date_str, '%Y%m%d')
        processed_data.append((date, amount_eur, amount_usd))
    processed_data.sort(key=lambda x: x[0])
    return processed_data

# Шаг 3: Привязка дат к ближайшим воскресеньям
def align_to_sundays(data):
    aligned_data = []
    for date, amount_eur, amount_usd in data:
        # Перенос даты на ближайшее прошлое воскресенье
        sunday = date - timedelta(days=date.weekday() + 1)
        aligned_data.append((sunday, amount_eur, amount_usd))
    return aligned_data

# Шаг 4: Добавление пропущенных воскресений и интерполяция данных
def fill_missing_sundays(data):
    filled_data = []
    current_date = data[0][0]
    end_date = data[-1][0]

    index = 0
    while current_date <= end_date:
        if index < len(data) and data[index][0] == current_date:
            filled_data.append(data[index])
            index += 1
        else:
            # Интерполяция между соседними значениями
            prev_date, prev_eur, prev_usd = filled_data[-1]
            next_date, next_eur, next_usd = data[index]
            days_diff = (next_date - prev_date).days
            interpolated_eur = prev_eur + (next_eur - prev_eur) * ((current_date - prev_date).days / days_diff)
            interpolated_usd = prev_usd + (next_usd - prev_usd) * ((current_date - prev_date).days / days_diff)
            filled_data.append((current_date, interpolated_eur, interpolated_usd))

        current_date += timedelta(days=7)  # Переход к следующему воскресенью

    return filled_data

# Шаг 5: Генерация line chart для Obsidian
def generate_chart(data):
    # chart_labels = "\n  - '" + "'\n  - '".join([date.strftime('%Y-%m-%d') for date, _, _ in data]) + "'"
    chart_labels = []
    chart_eur = []
    chart_usd = []

    for date, amount_eur, amount_usd in data:
        # Если это первое воскресенье месяца, подписываем месяц
        if date.day <= 7:
            chart_labels.append(date.strftime('%b'))
        else:
            chart_labels.append('')
        # Преобразование значений активов в целые числа
        chart_eur.append(int(amount_eur))
        chart_usd.append(int(amount_usd))

    # Генерация кода для графика Obsidian
    chart_code = f"""
    ```chart
    type: line
    labels: {chart_labels}
    series:
      - title: "Чистые активы в долларах"
        data: {chart_usd}
      - title: "Чистые активы в евро"
        data: {chart_eur}
    ```
    """
    return chart_code

# Основной процесс выполнения
def main():
    # Шаг 1: Извлечение данных
    data = fetch_recent_assets()

    # Шаг 2: Преобразование и сортировка дат
    processed_data = process_dates(data)

    # Шаг 3: Привязка к воскресеньям
    aligned_data = align_to_sundays(processed_data)

    # Шаг 4: Интерполяция пропущенных данных
    final_data = fill_missing_sundays(aligned_data)

    # Шаг 5: Генерация графика
    chart_code = generate_chart(final_data)
    print(chart_code)

if __name__ == "__main__":
    main()
