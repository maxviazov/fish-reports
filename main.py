#!/usr/bin/env python3
"""
Главный файл запуска Fish Reports System.
"""

import os
import sys
from pathlib import Path

# Добавляем путь к модулю
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Главная функция запуска."""
    try:
        from fish_reports.gui.main_window import FishReportsApp

        print("🐟 Запуск Fish Reports System...")
        print("=" * 40)

        app = FishReportsApp()
        app.run()

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
