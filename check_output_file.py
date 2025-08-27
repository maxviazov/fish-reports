import pandas as pd

# Читаем итоговый файл
output_file = 'test_output/ולדמן אשדוד.xlsx'
df_output = pd.read_excel(output_file)

print('=== ИТОГОВЫЙ ФАЙЛ: ולדמן אשדוד.xlsx ===')
print('Столбцы:', list(df_output.columns))
print('Первые 5 строк:')
print(df_output.head())
print()

# Ищем упоминание лицензии 512642182 или клиента "Вальдман Бат Ям"
print('Поиск лицензии 512642182 или клиента "Вальдман Бат Ям":')
found_rows = []

for idx, row in df_output.iterrows():
    row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])
    if '512642182' in row_str or 'Вальдман' in row_str or 'ולדמן' in row_str:
        found_rows.append((idx, row))

if found_rows:
    print(f'Найдено {len(found_rows)} строк с данными клиента:')
    for idx, row in found_rows:
        print(f'Строка {idx + 1}:')
        for col_name, value in row.items():
            if pd.notna(value):
                print(f'  {col_name}: {value}')
        print()
else:
    print('Данные клиента НЕ найдены в итоговом файле')
    print('Все уникальные значения в первых двух столбцах:')
    for col in df_output.columns[:2]:
        unique_vals = df_output[col].dropna().unique()[:10]  # Первые 10 уникальных
        print(f'{col}: {list(unique_vals)}')
