#!/usr/bin/env python3
"""
Тестирование группировки данных по базовому документу.
"""

import sys
import pandas as pd
from pathlib import Path

# Добавляем src к пути
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from fish_reports.data.file_processor import FileProcessor

def test_grouping():
    """Тестируем группировку данных по базовому документу."""
    
    # Создаем тестовый DataFrame - точно такой же как в реальных данных
    test_data = pd.DataFrame({
        'מספר עוסק מורשה': ['515926772', '515926772', '515926772', '34300798', '34300798', '516169083', '516169083'],
        'אסמכתת בסיס': ['223725', '223725', '129520', '223779', '223779', '223780', '223780'],
        'שם כרטיס': [
            'סופר פאפא חנויות מזון בע"מ - סניף רח\' קיבוץ גלוייות',
            'סופר פאפא חנויות מזון בע"מ - סניף רח\' קיבוץ גלוייות', 
            'סופר פאפא חנויות מזון בע"מ - סניף רח\' קיבוץ גלוייות',
            'קיוסק יהושוע',
            'קיוסק יהושוע',
            'אמי תל אביב בע"מ',
            'אמי תל אביב בע"מ'
        ],
        'שם לועזי': [
            'Супер Папа Хануйот Мазон баам Ашдод',
            'Супер Папа Хануйот Мазон баам Ашдод',
            'Супер Папа Хануйот Мазон баам Ашдод',
            'Киоск Егошуа Бат Ям',
            'Киоск Егошуа Бат Ям',
            'Эми Тель Авив Баам Бат Ям',
            'Эми Тель Авив Баам Бат Ям'
        ],
        'כתובת': [
            'אשדוד, קיבוץ גלוייות 1',
            'אשדוד, קיבוץ גלוייות 1',
            'אשדוד, קיבוץ גלוייות 1',
            'בת ים, יוספטל 97',
            'בת ים, יוספטל 97',
            'בת ים, יוספטל 33',
            'בת ים, יוספטל 33'
        ],
        'סה\'כ אריזות': [0.2, 0.13, 0.2, 0.2, 0.2, 0.2, 0.13],  # Уже в килограммах
        'סה\'כ משקל': [1.0, 1.0, 1.0, 0.8, 0.9, 0.9, 1.0]  # Уже в килограммах
    })
    
    print("Исходные данные:")
    print(test_data[['אסמכתת בסיס', 'מספר עוסק מורשה', 'סה\'כ אריזות', 'סה\'כ משקל']])
    print()
    
    # Создаем процессор файлов
    processor = FileProcessor()
    
    # Загружаем данные в процессор
    processor.filtered_data = test_data.copy()
    
    print("Группируем данные по אסמכתת בסיס...")
    success = processor.group_by_base_document()
    
    if not success:
        print("Ошибка при группировке!")
        return
    
    grouped_data = processor.filtered_data
    
    print("Данные после группировки:")
    print(grouped_data[['אסמכתת בסיס', 'מספר עוסק מורשה', 'סה\'כ אריזות', 'סה\'כ משקל']])
    print()
    
    # Проверяем группировку
    print("Проверка группировки:")
    unique_base_docs = test_data['אסמכתת בסיס'].unique()
    
    for base_doc in unique_base_docs:
        original_rows = test_data[test_data['אסמכתת בסיס'] == base_doc]
        grouped_row = grouped_data[grouped_data['אסמכתת בסיס'] == base_doc]
        
        if len(grouped_row) > 0:
            expected_packages = original_rows['סה\'כ אריזות'].sum()
            expected_weight = original_rows['סה\'כ משקל'].sum()
            
            actual_packages = grouped_row['סה\'כ אריזות'].iloc[0]
            actual_weight = grouped_row['סה\'כ משקל'].iloc[0]
            
            print(f"Базовый документ {base_doc}:")
            print(f"  Упаковки: {len(original_rows)} строк → 1 строка")
            print(f"  Сумма упаковок: {expected_packages:.2f} → {actual_packages:.2f} ({'✓' if abs(expected_packages - actual_packages) < 0.001 else '✗'})")
            print(f"  Сумма веса: {expected_weight:.2f} → {actual_weight:.2f} ({'✓' if abs(expected_weight - actual_weight) < 0.001 else '✗'})")
            print()

if __name__ == "__main__":
    test_grouping()
