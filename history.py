# history.py
import os, csv
from datetime import datetime

HISTORY_FILE = "prompt_history.csv"

def init_history_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Prompt", "Negative"])

def save_prompt_to_history(prompt: str, neg: str) -> None:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    next_id = str(len(lines)).zfill(2)  # 01, 02, 03...

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            next_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prompt or "",
            neg or ""
        ])

def read_history_table():
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows[1:]  # без заголовка

#def find_by_id(id_str: str) -> str:
    id_key = id_str.strip()
    for row in read_history_table():
        if row[0] == id_key:
            return f"ID {row[0]} | {row[1]}\nPrompt:\n{row[2]}\n\nNegative:\n{row[3]}"
    return "Not found"


def find_by_id(id_str: str):
    id_key = id_str.strip()
    for row in read_history_table():
        if row[0] == id_key:
            # row: [ID, Date, Prompt, Negative]
            return row[2], row[3]  # Prompt, Negative
    return "Not found", "Not found"


def clear_history():
    # перезаписываем файл заново с заголовками
    with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Prompt", "Negative"])
    return []  # возвращаем пустую таблицу



# инициализация при импорте
init_history_file()
