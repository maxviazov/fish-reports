#!/usr/bin/env python3
"""
Скрипт для запуска GUI версии Fish Reports System.
"""

import sys
from pathlib import Path

# Добавляем путь к модулю
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Запуск GUI версии."""
    try:
        from fish_reports.gui.main_window import FishReportsApp

        print("🐟 Запуск GUI версии Fish Reports System...")
        print("Если окно не появилось, проверьте панель задач")

        app = FishReportsApp()
        app.run()

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
