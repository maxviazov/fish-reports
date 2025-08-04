# Fish Reports Processing System

Система обработки отчетов о рыбе для Министерства здравоохранения Израиля.

## Описание

Приложение предназначено для:
1. Фильтрации данных из исходных файлов
2. Создания промежуточных файлов с отфильтрованными данными
3. Поиска и обновления файлов отчетов
4. Подготовки копий для отправки в משרד הבריאות

## Структура проекта

```
fish-reports-dolina/
├── src/
│   ├── fish_reports/
│   │   ├── __init__.py
│   │   ├── gui/
│   │   │   ├── __init__.py
│   │   │   └── main_window.py
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── file_processor.py
│   │   │   └── report_manager.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── file_utils.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
```bash
# Windows
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python -m src.fish_reports
```

## Разработка

Каждая новая функция разрабатывается в отдельной ветке:
- `feature/gui-setup` - настройка пользовательского интерфейса
- `feature/file-processing` - обработка файлов
- `feature/report-management` - управление отчетами

## Требования

- Python 3.8+
- tkinter (для GUI)
- pandas (для обработки данных)
- openpyxl (для работы с Excel файлами)
