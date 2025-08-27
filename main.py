#!/usr/bin/env python3
"""
Главный файл запуска Fish Reports System.
"""

import sys
from pathlib import Path

# Добавляем путь к модулю
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Главная функция запуска."""
    try:
        from fish_reports.core.workflow import FishReportsWorkflow

        print("🐟 Запуск Fish Reports System...")
        print("=" * 40)

        # Create workflow instance
        workflow = FishReportsWorkflow()

        # Set default paths (can be overridden by user)
        source_file = Path(r"C:\Users\office3\Desktop\FishKA\source\משקל.xlsx")
        intermediate_dir = Path(r"C:\Users\office3\Desktop\FishKA\filtered")
        reports_dir = Path(r"C:\Users\office3\Desktop\FishKA\reports")
        output_dir = Path(r"C:\Users\office3\Desktop\FishKA\output")

        # Set paths
        if not workflow.set_paths(source_file, intermediate_dir, reports_dir, output_dir):
            print("❌ Ошибка настройки путей")
            sys.exit(1)

        # Process files
        if workflow.process_files():
            print("✅ Обработка завершена успешно!")
            results = workflow.get_results()
            if results:
                print("\n📊 Результаты:")
                print(f"• Обработано строк: {results.get('total_rows', 0)}")
                print(f"• Общий вес (кг): {results.get('total_weight_kg', 0):.2f}")
                print(f"• Общее количество упаковок: {results.get('total_packages', 0)}")
                print(f"• Найдено лицензий: {results.get('unique_licenses', 0)}")
                print(f"• Скопировано файлов отчетов: {results.get('total_files', 0)}")
        else:
            print("❌ Ошибка при обработке файлов")
            sys.exit(1)

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
