import subprocess

def sync_folders(source_folder, destination_folder):
    # Создаем команду для синхронизации папок с помощью rsync
    command = ["rsync", "-avz", source_folder + "/", destination_folder + "/"]

    # Запускаем процесс синхронизации
    try:
        subprocess.run(command, check=True)
        print("Папки успешно синхронизированы!")
    except subprocess.CalledProcessError as e:
        print("Произошла ошибка при синхронизации папок:")
        print(e)

if __name__ == "__main__":
    # Указываем пути к исходной и целевой папкам
    source_folder = "/Users/user/Yandex.Disk-maksim.burdygin.localized/Obsidian vault"

    destination_folder = "/Users/user/Library/Mobile Documents/iCloud~md~obsidian/Documents/Max"

    # Вызываем функцию для синхронизации папок
    sync_folders(source_folder, destination_folder)
    sync_folders(destination_folder, source_folder)