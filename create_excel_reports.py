#!/usr/bin/env python3
"""
Создание примерных Excel файлов отчетов для тестирования.
"""

from pathlib import Path

import pandas as pd


def create_sample_excel_reports():
    """Создание примерных Excel файлов отчетов."""

    # Создаем папку для отчетов
    reports_dir = Path('sample_data/reports_excel')
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Данные для отчетов
    license_numbers = ["515926772", "34300798", "516169083", "512451451"]

    for license in license_numbers:
        # Создаем DataFrame для отчета
        report_data = {
            "שדה": [
                "מספר רישיון",
                "אסמכתת בסיס",
                "סה'כ אריזות",
                "סה'כ משקל",
                "שם כרטיס",
                "תאריך",
                "סטטוס"
            ],
            "ערך": [
                license,  # Лицензия
                "OLD_223044",  # Будет заменено
                "0",  # Будет заменено
                "7.0",  # Будет заменено
                "שם כרטיס לדוגמה",
                "04/08/2025",
                "פעיל"
            ]
        }

        df = pd.DataFrame(report_data)

        # Сохраняем в Excel
        report_file = reports_dir / f'report_{license}_2025.xlsx'
        df.to_excel(report_file, index=False, engine='openpyxl')

        print(f"✅ Создан Excel отчет: {report_file}")

    print(f"\n📁 Отчеты созданы в папке: {reports_dir}")

if __name__ == "__main__":
    print("Создание примерных Excel файлов отчетов...")
    create_sample_excel_reports()
    print("Готово!")
