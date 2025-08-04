"""
Sample data creation script for testing.
"""

import pandas as pd
from pathlib import Path


def create_sample_source_file():
    """Create a sample source file for testing."""
    data = {
        "מספר עוסק מורשה": [
            "515926772",
            "515926772",
            "515926772",
            "34300798",
            "34300798",
            "516169083",
            "516169083",
            "512451451",
            "512451451",
        ],
        "אסמכתת בסיס": [
            "223725",
            "223725",
            "129520",
            "223779",
            "223779",
            "223780",
            "223780",
            "129523",
            "129523",
        ],
        "שם כרטיס": [
            "סופר פאפא חנויות מזון בע\"מ - סניף רח' קיבוץ גלוייות",
            "סופר פאפא חנויות מזון בע\"מ - סניף רח' קיבוץ גלוייות",
            "סופר פאפא חנויות מזון בע\"מ - סניף רח' קיבוץ גלוייות",
            "קיוסק יהושוע",
            "קיוסק יהושוע",
            'אמי תל אביב בע"מ',
            'אמי תל אביב בע"מ',
            "רוסמן ק. אתא - מרכז",
            "רוסמן ק. אתא - מרכז",
        ],
        "שם לועזי": [
            "Супер Папа Хануйот Мазон баам Ашдод",
            "Супер Папа Хануйот Мазон баам Ашдод",
            "Супер Папа Хануйот Мазон баам Ашдод",
            "Киоск Егошуа Бат Ям",
            "Киоск Егошуа Бат Ям",
            "Эми Тель Авив Баам Бат Ям",
            "Эми Тель Авив Баам Бат Ям",
            "Росман-Кирьят Ата-Мерказ",
            "Росман-Кирьят Ата-Мерказ",
        ],
        "כתובת": [
            "אשדוד, קיבוץ גלוייות 1",
            "אשדוד, קיבוץ גלוייות 1",
            "אשדוד, קיבוץ גלוייות 1",
            "בת ים, יוספטל 97",
            "בת ים, יוספטל 97",
            "בת ים, יוספטל 33",
            "בת ים, יוספטל 33",
            "קרית אתא, חלוצי תעשיה 48",
            "קרית אתא, חלוצי תעשיה 48",
        ],
        "סה'כ אריזות": [
            200,
            130,
            200,
            200,
            200,
            200,
            130,
            400,
            400,
        ],  # Values in grams (0.2 = 200g, 0.13 = 130g, etc.)
        "סה'כ משקל": [
            1000,
            1000,
            1000,
            800,
            900,
            900,
            1000,
            2000,
            1600,
        ],  # Weights in grams
        "עמודה נוספת": [
            "נתון 1",
            "נתון 2",
            "נתון 3",
            "נתון 4",
            "נתון 5",
            "נתון 6",
            "נתון 7",
            "נתון 8",
            "נתון 9",
        ],
    }
    
    df = pd.DataFrame(data)
    
    # Create sample_data directory if it doesn't exist
    sample_dir = Path('sample_data')
    sample_dir.mkdir(exist_ok=True)
    
    # Save to Excel file
    output_file = sample_dir / 'sample_source_data.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Created sample source file: {output_file}")
    
    return output_file


def create_sample_reports():
    """Create sample report files for testing."""
    reports_dir = Path('sample_data/reports')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample report files with license numbers in names
    license_numbers = ["515926772", "34300798", "516169083", "512451451"]
    
    for license in license_numbers:
        # Create a simple text report file
        report_file = reports_dir / f'report_{license}_2025.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"דוח דגים עבור רישיון: {license}\n")
            f.write("=" * 30 + "\n")
            f.write("תאריך: 04/08/2025\n")
            f.write("סטטוס: פעיל\n")
            f.write("\nנתונים כלליים:\n")
            f.write("סה\"כ אריזות: 0\n")  # Will be updated
            f.write("סה\"כ משקל: 0\n")    # Will be updated
            f.write("אסמכתא: \n")        # Will be updated
        
        print(f"Created sample report: {report_file}")
    
    # Create one more report file without matching license
    extra_report = reports_dir / 'report_555555555_2025.txt'
    with open(extra_report, 'w', encoding='utf-8') as f:
        f.write("דוח נוסף ללא התאמה\n")
    
    print(f"Created extra report: {extra_report}")


if __name__ == "__main__":
    print("Creating sample data for Fish Reports application...")
    
    # Create sample source file
    source_file = create_sample_source_file()
    
    # Create sample reports
    create_sample_reports()
    
    print("\nSample data created successfully!")
    print(f"Source file: {source_file}")
    print("Reports directory: sample_data/reports/")
    print("\nYou can now use these files to test the application.")
