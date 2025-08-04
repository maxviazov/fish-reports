# Инструкции для GitHub

## 1. Создание приватного репозитория

1. Перейдите на https://github.com/maxviazov
2. Нажмите "New repository"
3. Название: `fish-reports-dolina`
4. Описание: `Fish Reports Processing System for Ministry of Health Israel`
5. Выберите "Private"
6. НЕ создавайте README (у нас уже есть)
7. НЕ добавляйте .gitignore (у нас уже есть)
8. Нажмите "Create repository"

## 2. Подключение локального репозитория

```bash
# Добавить remote origin
git remote add origin https://github.com/maxviazov/fish-reports-dolina.git

# Установить основную ветку
git branch -M main

# Отправить код на GitHub
git push -u origin main
```

## 3. Создание первой рабочей ветки

```bash
# Создать и переключиться на ветку для интеграции
git checkout -b feature/file-processing-integration

# Начать работу над интеграцией файловой обработки с GUI
```

## 4. Workflow для разработки

### Для каждой новой функции:

1. **Создать ветку от main:**
```bash
git checkout main
git pull origin main
git checkout -b feature/новая-функция
```

2. **Разработать функцию**
3. **Протестировать**
4. **Зафиксировать изменения:**
```bash
git add .
git commit -m "feat: краткое описание изменений"
```

5. **Отправить на GitHub:**
```bash
git push origin feature/новая-функция
```

6. **Создать Pull Request:**
   - Перейти на GitHub
   - Нажать "New Pull Request" 
   - Выбрать ветку feature/новая-функция -> main
   - Добавить описание изменений
   - Создать PR

7. **После ревью - слить в main:**
   - Нажать "Merge Pull Request"
   - Удалить ветку после слияния

## 5. Структура коммитов

Используйте conventional commits:
- `feat:` - новая функция
- `fix:` - исправление бага
- `docs:` - обновление документации
- `test:` - добавление тестов
- `refactor:` - рефакторинг кода
- `style:` - форматирование
- `chore:` - обновление зависимостей и т.д.

## 6. Текущий статус проекта

✅ **Завершено:**
- Базовая структура проекта
- GUI интерфейс для выбора директорий
- Компоненты обработки файлов
- Система управления отчетами
- Тестовые данные и примеры
- Настройка окружения разработки

🔄 **Следующие шаги:**
1. Интеграция компонентов обработки файлов с GUI
2. Реализация полного workflow
3. Улучшение обработки ошибок
4. Добавление тестов

## 7. Команды для быстрого старта

```bash
# Клонировать репозиторий (для других разработчиков)
git clone https://github.com/maxviazov/fish-reports-dolina.git
cd fish-reports-dolina

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать тестовые данные
python create_sample_data.py

# Запустить приложение
python -m src.fish_reports
```

Готово к загрузке на GitHub!
