#!/usr/bin/env python3
"""
Скрипт для тестирования Fish Reports System с примерными данными.
"""

import sys
from pathlib import Path

# Добавляем путь к модулю
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Тестирование с примерными данными."""
    try:
        from fish_reports.core.workflow import FishReportsWorkflow

        print("🐟 Тестирование Fish Reports System с примерными данными...")
        print("=" * 60)

        # Создаем workflow
        workflow = FishReportsWorkflow()

        # Устанавливаем пути к примерным данным
        source_file = current_dir / "sample_data" / "sample_source_data.xlsx"
        intermediate_dir = current_dir / "sample_data" / "filtered"
        reports_dir = current_dir / "sample_data" / "reports"
        output_dir = current_dir / "sample_data" / "output"

        print(f"📁 Исходный файл: {source_file}")
        print(f"📁 Промежуточные файлы: {intermediate_dir}")
        print(f"📁 Отчеты: {reports_dir}")
        print(f"📁 Результаты: {output_dir}")
        print()

        # Создаем папки, если они не существуют
        for dir_path in [intermediate_dir, reports_dir, output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Устанавливаем пути
        if not workflow.set_paths(source_file, intermediate_dir, reports_dir, output_dir):
            print("❌ Ошибка настройки путей")
            sys.exit(1)

        # Обрабатываем файлы
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

                if results.get('total_files', 0) > 0:
                    print("\n📋 Найденные отчеты:")
                    for license, files in results.get('files_by_license', {}).items():
                        print(f"  • Лицензия {license}: {len(files)} файл(ов)")
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
