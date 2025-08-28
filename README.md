# База данных фитнес клуба

## Описание проекта
Создание базы данных SQLite для сайта фитнес клуба с основными таблицами и связями между ними.

## Структура проекта

diploma_BODY_FIT/
├── database/
│ ├── fitness_club.db # Файл базы данных SQLite
│ ├── init_db.py # Скрипт создания базы данных
│ ├── execute_sql.py # Скрипт выполнения SQL запросов
│ └── check_data.py # Скрипт проверки данных
├── sql_scripts/
│ ├── create_database.sql # Создание таблиц
│ ├── update_structure.sql # Обновление структуры
│ ├── insert_data.sql # Вставка данных
│ ├── clear_all.sql # Очистка базы данных
│ └── final_database.sql # Итоговый SQL файл
├── requirements.txt # Зависимости Python
└── README.md # Документация


## Созданные таблицы
1. **trainers** - Тренера (29 записей)
2. **workouts** - Тренировки (20 записей)
3. **clients** - Клиенты (20 записей)
4. **appointments** - Записи на тренировки (4 записи)
5. **trainers_workouts** - Связь тренеров и тренировок (33 записи)
6. **appointments_workouts** - Связь записей и тренировок (4 записи)

## Порядок полей в таблицах
- **trainers**: last_name, first_name, middle_name, name_of_training_session
- **workouts**: name_of_training_session, last_name, first_name, middle_name, description
- **clients**: last_name, first_name, middle_name, phone, name_of_training_session
- **appointments**: last_name, first_name, phone, date, trener_id, name_of_training_session

## Запуск проекта
1. Активировать виртуальное окружение: `venv\Scripts\Activate.ps1`
2. Создать базу данных: `python database/init_db.py`
3. Выполнить SQL скрипт: `python database/execute_sql.py sql_scripts/final_database.sql`
4. Проверить данные: `python database/check_data.py`

## Требования
- Python 3.8+
- SQLite3
- Flask (для веб-интерфейса)