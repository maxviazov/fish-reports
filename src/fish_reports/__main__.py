"""
Entry point for the Fish Reports application.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the application."""
    from fish_reports.core.workflow import FishReportsWorkflow

    # Create workflow instance
    workflow = FishReportsWorkflow()

    # Set default paths (can be overridden by user)
    source_file = Path(r"C:\Users\office3\Desktop\FishKA\source\משקל.xlsx")
    intermediate_dir = Path(r"C:\Users\office3\Desktop\FishKA\filtered")
    reports_dir = Path(r"C:\Users\office3\Desktop\FishKA\reports")
    output_dir = Path(r"C:\Users\office3\Desktop\FishKA\output")

    print("🐟 Запуск Fish Reports System...")
    print("=" * 40)

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

if __name__ == "__main__":
    main()
