import os
import speech_recognition as sr

# Загрузка списка приложений из файла
APP_LIST_PATH = "exe_files_list.txt"

def load_app_list(file_path):
    """Загружает список приложений из файла."""
    app_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    app_name, app_path = line.split(": ", 1)
                    app_dict[app_name.strip()] = app_path.strip()
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Убедитесь, что он существует.")
    except Exception as e:
        print(f"Ошибка при загрузке списка приложений: {e}")
    return app_dict

def recognize_speech(prompt=""):
    """Распознавание речи и возвращение команды."""
    if prompt:
        print(prompt)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            return r.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")
            return None
        except sr.RequestError as e:
            print(f"Ошибка соединения: {e}")
            return None

def execute_command(command, app_dict):
    """Обработка команды запуска приложений."""
    try:
        if command.startswith("запусти"):
            app_name = command.replace("запусти", "").strip()
            if app_name in app_dict:
                app_path = app_dict[app_name]
                print(f"Запускаю {app_name} из {app_path}")
                os.startfile(app_path)
            else:
                print(f"Приложение с именем '{app_name}' не найдено в списке.")
        elif command == "покажи приложения":
            print("Доступные приложения:")
            for name in app_dict.keys():
                print(f"- {name}")
        elif command in ["стоп", "выход"]:
            print("Останавливаю программу.")
            exit()
        else:
            print(f"Неизвестная команда: {command}")
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")

if __name__ == "__main__":
    print("Загрузка списка приложений...")
    app_dict = load_app_list(APP_LIST_PATH)

    if not app_dict:
        print("Список приложений пуст или отсутствует. Завершение работы.")
        exit()

    print("Программа запущена. Скажите команду, например: 'запусти chrome'.")
    while True:
        command = recognize_speech("Слушаю вашу команду...")
        if command:
            print(f"Распознано: {command}")
            execute_command(command, app_dict)
