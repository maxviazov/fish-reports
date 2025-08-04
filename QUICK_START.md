# 🚀 Быстрый запуск Fish Reports

## Для Windows PowerShell:

### Способ 1 (пошагово):
```powershell
cd c:\Users\office3\Documents\Project\fish-reports-dolina
.\venv\Scripts\activate
cd src
python -m fish_reports
```

### Способ 2 (одной командой):
```powershell
cd src ; python -m fish_reports
```

## Для тестирования:

### Полный тест workflow:
```powershell
python test_full_workflow.py
```

### Тест группировки:
```powershell
python test_grouping.py
```

### Создание тестовых данных:
```powershell
python create_sample_data.py
```

## ⚠️ Важно!

В PowerShell используйте `;` вместо `&&` для разделения команд:
- ❌ `cd src && python -m fish_reports`
- ✅ `cd src ; python -m fish_reports`

---
*Готово к запуску!* 🎯
