import sys
from pathlib import Path

import pandas as pd

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from fish_reports.data.report_manager import ReportManager


def test_field_replacement():
    """Test the updated field replacement logic."""

    # Test data from intermediate file
    test_replacement_data = {
        'אסמכתת בסיס': 226239,
        'סה\'כ אריזות': 0.2,
        'סה\'כ משקל': 1,
        'שם כרטיס': 'Вальдман Бат Ям'
    }

    print("=== ТЕСТИРОВАНИЕ ОБНОВЛЕННОЙ ЛОГИКИ ЗАМЕНЫ ПОЛЕЙ ===")
    print(f"Тестовые данные: {test_replacement_data}")
    print()

    # Create report manager
    reports_dir = Path("sample_data/reports_excel")
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)

    manager = ReportManager(reports_dir, output_dir)

    # Test field mappings
    field_mappings = manager._get_field_mappings()
    print("Field mappings:")
    for k, v in field_mappings.items():
        print(f"  '{k}' -> '{v}'")
    print()

    # Simulate field replacements configuration
    field_replacements = [
        # אסמכתת בסיס -> מספר תעודת משלוח
        {
            'intermediate_field': 'אסמכתת בסיס',
            'search_fields': ['מספר תעודת משלוח', 'אסמכתת בסיס', 'מספר תעודת משלוח'],
            'replace_value': str(test_replacement_data.get('אסמכתת בסיס', ''))
        },
        # סה'כ משקל -> מוצרים מוכנים לאכילה
        {
            'intermediate_field': 'סה\'כ משקל',
            'search_fields': ['מוצרים מוכנים לאכילה', 'סה\'כ משקל', 'סהכ משקל', 'מוצרים מוכנים לאכילה'],
            'replace_value': str(test_replacement_data.get('סה\'כ משקל', test_replacement_data.get('סהכ משקל', '')))
        },
        # סה'כ אריזות -> סה"כ קרטונים
        {
            'intermediate_field': 'סה\'כ אריזות',
            'search_fields': ['סה"כ קרטונים', 'סה\'כ אריזות', 'סהכ אריזות', 'סה"כ קרטונים'],
            'replace_value': str(test_replacement_data.get('סה\'כ אריזות', test_replacement_data.get('סהכ אריזות', '')))
        }
    ]

    print("Конфигурация замен:")
    for replacement in field_replacements:
        print(f"  {replacement['intermediate_field']} -> {replacement['search_fields']} : '{replacement['replace_value']}'")
    print()

    # Test with actual file
    source_file = Path("test_output/ולדמן אשדוד.xlsx")
    if source_file.exists():
        print(f"Тестируем с файлом: {source_file}")
        dest_file = Path("test_output/ולדמן אשדוד_test.xlsx")

        success = manager._copy_file_with_replacement(source_file, dest_file, test_replacement_data)
        if success:
            print("✅ Тест завершен успешно")
            print(f"Результат сохранен в: {dest_file}")

            # Check results
            df_result = pd.read_excel(dest_file)
            print("\\nРезультаты замены:")

            # Check specific fields
            for replacement in field_replacements:
                for search_field in replacement['search_fields']:
                    if search_field in df_result.columns:
                        values = df_result[search_field].dropna().tolist()
                        print(f"  {search_field}: {values}")
        else:
            print("❌ Ошибка при тестировании")
    else:
        print(f"❌ Файл {source_file} не найден")

if __name__ == "__main__":
    test_field_replacement()
