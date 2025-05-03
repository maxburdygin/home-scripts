import csv
from collections import defaultdict

def process_transactions(file_path):
    transactions = defaultdict(list)
    category_totals = defaultdict(float)

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Пропустить первую строку

        for row in reader:
            if len(row) < 10:
                continue

            category = row[1] if row[1] else "Без категории"
            payee = row[2] if row[2] else ""
            comment = row[3] if row[3] else ""
            outcome = -float(row[5].replace(',', '.') if row[5] else 0)
            income = float(row[8].replace(',', '.') if row[8] else 0)
            amount = outcome + income

            transactions[category].append(f"- {payee} ({comment}): {amount:.2f} RUB")
            category_totals[category] += amount

    return transactions, category_totals

def generate_markdown(transactions, category_totals):
    markdown_lines = []

    for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        markdown_lines.append(f"### {category} ({total:.2f} RUB)")
        markdown_lines.extend(transactions[category]).append("\n")

    return "\n".join(markdown_lines)

# Использование
file_path = "/Users/user/Downloads/Telegram Desktop/zen_2025-02-22_8231AB97.csv"
transactions, category_totals = process_transactions(file_path)
markdown_output = generate_markdown(transactions, category_totals)

# Сохранение в файл
with open("/Users/user/Downloads/Telegram Desktop/zen_2025-02-22.md", "w", encoding="utf-8") as md_file:
    md_file.write(markdown_output)