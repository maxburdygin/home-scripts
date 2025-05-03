CREATE TABLE IF NOT EXISTS budget_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- Название заметки (например, "20231001 Бюджет")
    comment TEXT,  -- Комментарий к заметке
    created_date TEXT NOT NULL,  -- Дата создания заметки (в формате YYYY-MM-DD)
    updated_date TEXT NOT NULL  -- Дата последнего обновления заметки
);