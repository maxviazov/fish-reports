#!/usr/bin/env python3
"""
Полный тест workflow с группировкой данных.
"""

import sys
import pandas as pd
from pathlib import Path

# Добавляем src к пути
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from fish_reports.core.workflow import FishReportsWorkflow

def test_full_workflow():
    """Тестируем полный workflow с группировкой."""
    
    print("=== ПОЛНЫЙ ТЕСТ WORKFLOW ===")
    print()
    
    # Используем существующие тестовые данные
    source_file = Path("sample_data/sample_source_data.xlsx")
    intermediate_dir = Path("C:/Users/office3/Desktop/FishKA/intermediate")
    reports_dir = Path("sample_data/reports")
    output_dir = Path("C:/Users/office3/Desktop/FishKA/output")
    
    if not source_file.exists():
        print(f"Источник данных не найден: {source_file}")
        print("Запустите 'python create_sample_data.py' для создания тестовых данных.")
        return
    
    # Создаем workflow
    workflow = FishReportsWorkflow()
    
    # Устанавливаем пути
    print("Устанавливаем пути...")
    success = workflow.set_paths(source_file, intermediate_dir, reports_dir, output_dir)
    if not success:
        print("Ошибка при установке путей!")
        return
    
    print("Пути установлены успешно.")
    print()
    
    # Обрабатываем файлы
    print("Запускаем обработку файлов...")
    success = workflow.process_files()
    
    if success:
        print("✓ Обработка файлов завершена успешно!")
        
        # Проверяем результаты
        intermediate_file = intermediate_dir / "filtered_data.xlsx"
        if intermediate_file.exists():
            print(f"✓ Промежуточный файл создан: {intermediate_file}")
            
            # Читаем и показываем результаты
            df = pd.read_excel(intermediate_file)
            print(f"✓ Итоговых строк после группировки: {len(df)}")
            
            total_weight = df['סה\'כ משקל'].sum()
            total_packages = df['סה\'כ אריזות'].sum()
            print(f"✓ Общий вес: {total_weight:.2f} кг")
            print(f"✓ Общее количество упаковок: {total_packages:.2f}")
            
            print("\nИтоговые данные по базовым документам:")
            print(df[['אסמכתת בסיס', 'מספר עוסק מורשה', 'סה\'כ אריזות', 'סה\'כ משקל']])
        else:
            print("⚠ Промежуточный файл не найден")
    else:
        print("✗ Ошибка при обработке файлов!")

if __name__ == "__main__":
    test_full_workflow()
