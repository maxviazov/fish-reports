import pandas as pd

# Читаем промежуточный файл
intermediate_file = 'test_output/filtered_data.xlsx'
df_intermediate = pd.read_excel(intermediate_file)

print('=== ПРОМЕЖУТОЧНЫЙ ФАЙЛ: filtered_data.xlsx ===')
print('Столбцы:', list(df_intermediate.columns))
print()

# Ищем клиента с лицензией 512642182
license_records = df_intermediate[df_intermediate['ח"פ לקוח או מספר עוסק'] == 512642182]
if not license_records.empty:
    print('Найдена запись для лицензии 512642182:')
    for _, row in license_records.iterrows():
        base_doc = row['אסמכתת בסיס']
        client_name = row['שם כרטיס']
        packages = row["סה'כ אריזות"]
        weight = row["סה'כ משקל"]
        print(f'אסמכתת בסיס: {base_doc}')
        print(f'שם כרטיס: {client_name}')
        print(f'סה"כ אריזות: {packages}')
        print(f'סה"כ משקל: {weight}')
        print()
else:
    print('Запись для лицензии 512642182 НЕ найдена в промежуточном файле')
    print('Все лицензии в файле:')
    licenses = df_intermediate['ח"פ לקוח או מספר עוסק'].unique()
    for lic in licenses:
        print(f'  {lic}')
