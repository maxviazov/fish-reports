import pandas as pd

# Читаем оба файла
intermediate_file = 'test_output/filtered_data.xlsx'
output_file = 'test_output/ולדמן אשדוד.xlsx'

df_intermediate = pd.read_excel(intermediate_file)
df_output = pd.read_excel(output_file)

print('=== СРАВНЕНИЕ ДАННЫХ ДЛЯ ЛИЦЕНЗИИ 512642182 ===')
print()

# Данные из промежуточного файла
license_records = df_intermediate[df_intermediate['ח"פ לקוח או מספר עוסק'] == 512642182]
if not license_records.empty:
    row = license_records.iloc[0]
    print('ПРОМЕЖУТОЧНЫЙ ФАЙЛ:')
    packages_col = "סה'כ אריזות"
    weight_col = "סה'כ משקל"
    cartons_col = "סה\"כ קרטונים"
    # license_col = "ח\"פ לקוח \\nאו מספר אישור משרד הבריאות במקרים בהם המשלוח הוא למפעל מאושר"

    print(f'  אסמכתת בסיס: {row["אסמכתת בסיס"]}')
    print(f'  {packages_col}: {row[packages_col]}')
    print(f'  {weight_col}: {row[weight_col]}')
    print(f'  שם כרטיס: {row["שם כרטיס"]}')
    print()

# Данные из итогового файла
print('ИТОГОВЫЙ ФАЙЛ:')
output_row = df_output.iloc[0]  # Первая строка
print(f'  מספר תעודת משלוח: {output_row["מספר תעודת משלוח"]}')
print(f'  מוצרים מוכנים לאכילה: {output_row["מוצרים מוכנים לאכילה"]}')
print(f'  {cartons_col}: {output_row[cartons_col]}')
print(f'  לקוח: {output_row["לקוח"]}')
# print(f'  ח"פ לקוח: {output_row["ח\"פ לקוח \\nאו מספר אישור משרד הבריאות במקרים בהם המשלוח הוא למפעל מאושר"]}')
print()

print('=== АНАЛИЗ ИЗМЕНЕНИЙ ===')

# Проверяем, есть ли в итоговом файле поля, которые должны были быть заменены
expected_fields = ['אסמכתת בסיס', 'סה\'כ אריזות', 'סה\'כ משקל']
found_fields = []
not_found_fields = []

for field in expected_fields:
    if field in df_output.columns:
        found_fields.append(field)
    else:
        not_found_fields.append(field)

print(f'Ожидаемые поля для замены: {expected_fields}')
print(f'Найденные поля: {found_fields}')
print(f'Отсутствующие поля: {not_found_fields}')

if found_fields:
    print('\\nЗначения найденных полей:')
    for field in found_fields:
        value = output_row[field] if field in output_row else 'N/A'
        print(f'  {field}: {value}')

print('\\n=== ВЫВОД ===')
if not found_fields:
    print('❌ В итоговом файле НЕ найдены поля, которые должны были быть заменены')
    print('Это означает, что замена данных не произошла или произошла в другие поля')
else:
    print('✅ В итоговом файле найдены некоторые поля для замены')
    print('Нужно проверить, совпадают ли значения с промежуточным файлом')
