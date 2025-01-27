import speech_recognition as sr
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

KEYWORDS = ["ассистент", "assistant", "компьютер", "бот", "флот", "flout", "float"]  # Список ключевых слов

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
            return None
        except sr.RequestError as e:
            print(f"Ошибка соединения: {e}")
            return None

def open_browser(browser_name):
    """Открытие браузера."""
    browsers = {"opera": "opera.exe", "chrome": "chrome.exe"}
    path = browsers.get(browser_name.lower())
    if path:
        try:
            os.startfile(path)
        except FileNotFoundError:
            print(f"Не удалось найти {browser_name}.exe")
    else:
        print(f"Браузер {browser_name} не поддерживается.")

def run_adblock():
    """Запуск скрипта AdBlock."""
    path = r"C:\Users\illar\OneDrive\Desktop\s\zapret-discord-youtube-main\general (ALT2).bat"
    try:
        os.startfile(path)
    except FileNotFoundError:
        print("Скрипт AdBlock не найден.")

def search_internet(query):
    """Поиск в интернете."""
    query = query.strip()
    if query:
        webbrowser.open(f"https://yandex.ru/search/?text={query}")
    else:
        print("Пустой запрос для поиска.")

def search_youtube(video_name):
    """Поиск видео на YouTube и запуск первого доступного результата."""
    video_name = video_name.strip()
    if not video_name:
        print("Название видео не указано. Открываю YouTube.")
        webbrowser.open("https://www.youtube.com")
        return

    print(f"Ищу видео на YouTube: {video_name}")
    query = video_name.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим первую ссылку на видео
        video_tag = soup.find('a', href=True, attrs={"aria-hidden": "true"})
        if video_tag and "/watch?v=" in video_tag['href']:
            video_url = f"https://www.youtube.com{video_tag['href'].split('&')[0]}"
            webbrowser.open(video_url)
            print(f"Запускаю видео: {video_name}")
        else:
            print("Видео не найдено. Открываю результаты поиска на YouTube.")
            webbrowser.open(url)
    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except Exception as e:
        print(f"Ошибка при поиске видео: {e}")

def list_audio_devices():
    """Выводит список доступных аудиоустройств."""
    devices = AudioUtilities.GetAllDevices()
    print("Доступные аудиоустройства:")
    for i, device in enumerate(devices, 1):
        print(f"{i}. {device.FriendlyName}")

def shutdown_computer():
    """Выключение компьютера."""
    print("Выключаю компьютер...")
    os.system("shutdown /s /t 1")

def restart_computer():
    """Перезапуск компьютера."""
    print("Перезапускаю компьютер...")
    os.system("shutdown /r /t 1")

def switch_audio_device(device_name):
    """Переключение аудиоустройства вывода."""
    devices = AudioUtilities.GetAllDevices()
    found = False

    for device in devices:
        if device.FriendlyName.lower() == device_name.lower():
            print(f"Переключаю вывод звука на: {device.FriendlyName}")
            interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(0, None)  # Снимаем mute
            found = True
            break

    if not found:
        print(f"Устройство с названием '{device_name}' не найдено. Вы можете использовать:")
        list_audio_devices()

def execute_command(command):
    """Обработка одной команды."""
    try:
        if 'оперу' in command:
            open_browser("opera")
        elif 'chrome' in command:
            open_browser("chrome")
        elif 'adblock' in command:
            run_adblock()
        elif 'выключи компьютер' in command or 'выключить компьютер' in command:
            shutdown_computer()
        elif 'перезапусти компьютер' in command or 'перезапуск компьютера' in command:
            restart_computer()
        elif 'youtube' in command or 'ютубе' in command:
            video_name = command.replace(command[:command.index('youtube') + 7], '').strip()
            search_youtube(video_name)
        elif 'найди' in command or 'открой' in command:
            query = command.replace('найди', '').replace('открой', '').strip()
            search_internet(query)
        elif 'наушники' in command:
            device_name = "G432 Gaming Headset"
            switch_audio_device(device_name)
        elif 'динамики' in command or 'колонки' in command:
            device_name = "Digital Audio (HDMI) (High Definition Audio Device)"
            switch_audio_device(device_name)
        elif 'стоп' in command or 'stop' in command or 'останови программу' in command:
            print("Останавливаю программу.")
            exit()
        elif 'discord' in command:
            os.startfile(r"E:\Discord\app-1.0.9179\Discord.exe")
        elif 'иди на хуй' in command:
            print("Сам иди")
        elif 'протокол 1' in command:
            run_adblock()
            os.startfile(r"E:\Discord\app-1.0.9179\Discord.exe")
            open_browser("opera")
        else:
            print(f"Неизвестная команда: {command}")
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")

if __name__ == "__main__":
    print(f"Жду команд")
    while True:
        # Ждём ключевое слово
        command = recognize_speech()
        if command and any(keyword in command for keyword in KEYWORDS):
            print("Я вас услышал! Скажите команду.")
            # Слушаем команду после ключевого слова
            follow_up_command = recognize_speech("Слушаю вашу команду...")
            if follow_up_command:
                print(f"Распознано: {follow_up_command}")
                execute_command(follow_up_command)
            else:
                print("Команда не была распознана.")
