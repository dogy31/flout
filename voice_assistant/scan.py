import os

def scan_for_exe_files(drive_paths, output_file):
    """Сканирует указанные диски на наличие .exe файлов и сохраняет результаты в файл без дубликатов."""
    try:
        seen_files = set()  # Для предотвращения повторений
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("# Список программ для запуска\n")
            for drive in drive_paths:
                print(f"Сканирование диска: {drive}")
                for root, dirs, files in os.walk(drive):
                    for name in files:
                        if name.endswith(".exe"):
                            program_name = name[:-4].lower()  # Убираем '.exe' и приводим к нижнему регистру
                            full_path = os.path.join(root, name)
                            if program_name not in seen_files:
                                seen_files.add(program_name)
                                file.write(f"{program_name}: {full_path}\n")
                                print(f"Добавлено: {program_name} -> {full_path}")
        print(f"Сканирование завершено. Результаты сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сканировании: {e}")

if __name__ == "__main__":
    # Получение списка всех доступных дисков
    drives = [f"{chr(d)}:\\" for d in range(65, 91) if os.path.exists(f"{chr(d)}:\\")]
    output_filename = "exe_files_list.txt"

    print(f"Обнаруженные диски: {', '.join(drives)}")
    print("Начинаем сканирование на наличие .exe файлов...")
    scan_for_exe_files(drives, output_filename)
