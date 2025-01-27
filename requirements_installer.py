import subprocess
import sys

# Список необходимых библиотек
libraries = [
    "speechrecognition",
    "requests",
    "beautifulsoup4",
    "pycaw",
    "comtypes",
    "googletrans==4.0.0-rc1",  # Указываем стабильную версию
    "asyncio"
]

def install_libraries():
    """Устанавливает все библиотеки из списка."""
    for library in libraries:
        try:
            print(f"Устанавливаю {library}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при установке {library}: {e}")
        else:
            print(f"{library} успешно установлена.")

if __name__ == "__main__":
    install_libraries()
