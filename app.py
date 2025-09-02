#!/usr/bin/env python3
"""
Основной файл для запуска приложения Fish Reports System.
Этот файл используется для создания исполняемого файла Windows.
"""

import os
import sys
from pathlib import Path


def setup_environment():
    """Настройка путей и переменных окружения."""
    # Добавляем путь к модулю
    if getattr(sys, 'frozen', False):
        # Запущено как exe
        base_path = Path(sys._MEIPASS)
        # В exe все файлы находятся в корне
        sys.path.insert(0, str(base_path))
    else:
        # Запущено как .py
        base_path = Path(__file__).parent
        # Добавляем путь к src
        src_path = base_path / 'src'
        if src_path.exists():
            sys.path.insert(0, str(src_path))

def main():
    """Главная функция запуска приложения."""
    try:
        setup_environment()
        from fish_reports.gui.main_window import FishReportsApp

        print("🐟 Запуск Fish Reports System...")
        print("Если окно не появилось, проверьте панель задач")

        app = FishReportsApp()
        app.run()

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
