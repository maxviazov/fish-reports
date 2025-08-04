"""
Sample data creation script for testing.
"""

import pandas as pd
from pathlib import Path


def create_sample_source_file():
    """Create a sample source file for testing."""
    data = {
        'מספר עוסק מורשה': ['123456789', '987654321', '456789123', '789123456', '321654987'],
        'אסמכתת בסיס': ['REF-2025-001', 'REF-2025-002', 'REF-2025-003', 'REF-2025-004', 'REF-2025-005'],
        'שם כרטיס': ['דגי ים תיכון בע"מ', 'חברת הדייגים בע"מ', 'דגי הצפון לטד', 'חוות דגים דרומיים', 'דגי ישראל בע"מ'],
        'שם לועזי': ['Mediterranean Fish Ltd', 'Fishermen Company Ltd', 'North Fish Ltd', 'Southern Fish Farm', 'Israel Fish Ltd'],
        'כתובת': ['רח\' הדייגים 10, תל אביב', 'רח\' הנמל 25, חיפה', 'רח\' הים 5, נהריה', 'קיבוץ דגניה א\'', 'רח\' הרצל 33, אשדוד'],
        'סה\'כ אריזות': [50, 75, -10, 120, 30],  # One negative value
        'סה\'כ משקל': [500.5, 750.25, -100.0, 1200.75, 300.0],  # One negative value
        'עמודה נוספת': ['נתון 1', 'נתון 2', 'נתון 3', 'נתון 4', 'נתון 5']  # Extra column
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
    license_numbers = ['123456789', '987654321', '456789123']
    
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
