import pandas as pd

# Сравниваем оригинальный и тестовый файлы
original_file = 'test_output/ולדמן אשדוד.xlsx'
test_file = 'test_output/ולדמן אשדוד_test.xlsx'

print("=== СРАВНЕНИЕ ОРИГИНАЛЬНОГО И ТЕСТОВОГО ФАЙЛОВ ===")

df_original = pd.read_excel(original_file)
df_test = pd.read_excel(test_file)

print("Оригинальный файл:")
original_row = df_original.iloc[0]
cartons_col = "סה\"כ קרטונים"
print(f"  מספר תעודת משלוח: {original_row['מספר תעודת משלוח']}")
print(f"  מוצרים מוכנים לאכילה: {original_row['מוצרים מוכנים לאכילה']}")
print(f"  {cartons_col}: {original_row[cartons_col]}")
print()

print("Тестовый файл после замены:")
test_row = df_test.iloc[0]
print(f"  מספר תעודת משלוח: {test_row['מספר תעודת משלוח']}")
print(f"  מוצרים מוכנים לאכילה: {test_row['מוצרים מוכנים לאכילה']}")
print(f"  {cartons_col}: {test_row[cartons_col]}")
print()

print("Ожидаемые значения для замены:")
print("  מספר תעודת משלוח: 226239 (было 213118)")
print("  מוצרים מוכנים לאכילה: 1 (было 15.9)")
print("  סה\"כ קרטונים: 0.2 (было 2.75)")
print()

# Проверяем, произошла ли замена
replacements_made = 0
if str(test_row['מספר תעודת משלוח']) == '226239':
    print("✅ מספר תעודת משלוח: ЗАМЕНА ПРОИЗОШЛА (213118 -> 226239)")
    replacements_made += 1
else:
    print("❌ מספר תעודת משלוח: замена НЕ произошла")

if str(test_row['מוצרים מוכנים לאכילה']) == '1':
    print("✅ מוצרים מוכנים לאכילה: ЗАМЕНА ПРОИЗОШЛА (15.9 -> 1)")
    replacements_made += 1
else:
    print("❌ מוצרים מוכנים לאכילה: замена НЕ произошла")

if str(test_row[cartons_col]) == '0.2':
    print("✅ סה\"כ קרטונים: ЗАМЕНА ПРОИЗОШЛА (2.75 -> 0.2)")
    replacements_made += 1
else:
    print("❌ סה\"כ קרטונים: замена НЕ произошла")

print(f"\\nВсего успешных замен: {replacements_made}/3")

if replacements_made == 3:
    print("🎉 ВСЕ ЗАМЕНЫ ПРОИЗОШЛИ УСПЕШНО!")
else:
    print("⚠️  Некоторые замены не произошли")
