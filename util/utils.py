import argparse
from util.constants import CONFIG_FILE_PATH

def read_param_from_config(param_name):
    with open(CONFIG_FILE_PATH, 'r') as file:
        for line in file:
            if line.startswith(f"{param_name}="):
                return line.split("=", 1)[1].strip()
    return None

def update_param_in_config(param_name, new_value):
    lines = []
    param_found = False

    # Чтение файла и обновление значения параметра
    with open(CONFIG_FILE_PATH, 'r') as file:
        for line in file:
            if line.startswith(f"{param_name}="):
                lines.append(f"{param_name}={new_value}\n")
                param_found = True
            else:
                lines.append(line)

    # Если параметр не найден, добавить его в конец
    if not param_found:
        lines.append(f"\n{param_name}={new_value}")

    # Перезапись файла с обновленным содержимым
    with open(CONFIG_FILE_PATH, 'w') as file:
        file.writelines(lines)

# Добавление поддержки командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update parameter in config file")
    parser.add_argument('param_name', type=str, help="Name of the parameter to update")
    parser.add_argument('new_value', type=str, help="New value for the parameter")
    args = parser.parse_args()

    update_param_in_config(args.param_name, args.new_value)
