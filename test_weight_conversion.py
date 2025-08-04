#!/usr/bin/env python3
"""
Тестирование конвертации веса из граммов в килограммы.
"""

import sys
import pandas as pd
from pathlib import Path

# Добавляем src к пути
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from fish_reports.data.file_processor import FileProcessor

def test_weight_conversion():
    """Тестируем конвертацию веса."""
    
    # Создаем тестовый DataFrame с весами в граммах
    test_data = pd.DataFrame({
        'מספר עוסק מורשה': ['123456789', '987654321', '456789123'],
        'כ ממ במחסן ג': [1000, 4500, 2300],  # вес в граммах
        'אסמכתת בסיס': ['doc1', 'doc2', 'doc3'],
        'כמ אריזות במחסן': [10, 15, 20]
    })
    
    print("Исходные данные (вес в граммах):")
    print(test_data)
    print()
    
    # Создаем процессор файлов
    processor = FileProcessor()
    
    # Загружаем данные в процессор
    processor.filtered_data = test_data.copy()
    
    # Конвертируем вес
    success = processor.convert_to_kilograms()
    
    if not success:
        print("Ошибка при конвертации!")
        return
    
    converted_data = processor.filtered_data
    
    print("Данные после конвертации (вес в килограммах):")
    print(converted_data)
    print()
    
    # Проверяем конвертацию
    original_weights = test_data['כ ממ במחסן ג'].tolist()
    converted_weights = converted_data['כ ממ במחסן ג'].tolist()
    
    print("Проверка конвертации:")
    for orig, conv in zip(original_weights, converted_weights):
        expected = orig / 1000.0
        print(f"{orig}г → {conv}кг (ожидалось: {expected}кг) - {'✓' if abs(conv - expected) < 0.001 else '✗'}")

if __name__ == "__main__":
    test_weight_conversion()
