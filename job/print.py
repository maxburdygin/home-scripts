import os

def print_files_in_folder(folder_path):
    # Проверяем, существует ли указанная папка
    if not os.path.exists(folder_path):
        print(f"Папка '{folder_path}' не существует.")
        return

    # Получаем список файлов в указанной папке
    files = os.listdir(folder_path)

    # Выводим имена всех файлов
    print(f"Файлы в папке '{folder_path}':")
    for file_name in files:
        print(file_name)

if __name__ == "__main__":
    folder_path = input("Введите путь к папке: ")
    print_files_in_folder(folder_path)
