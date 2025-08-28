import sqlite3
import os
import sys

def execute_sql_script(sql_file_path=None):
    # Путь к файлу базы данных
    db_path = os.path.join(os.path.dirname(__file__), 'fitness_club.db')
    
    # Путь к SQL файлу (по умолчанию или переданный параметр)
    if sql_file_path:
        sql_path = sql_file_path
    else:
        sql_path = os.path.join(os.path.dirname(__file__), '..', 'sql_scripts', 'create_database.sql')
    
    # Создание соединения с базой данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Чтение SQL файла
        with open(sql_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Выполнение SQL скрипта
        cursor.executescript(sql_script)
        
        # Подтверждение изменений
        conn.commit()
        
        print(f"SQL скрипт {sql_path} выполнен успешно!")
        print("Таблицы обновлены в базе данных.")
        
    except Exception as e:
        print(f"Ошибка при выполнении SQL скрипта: {e}")
        conn.rollback()
    
    finally:
        # Закрытие соединения
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_sql_script(sys.argv[1])
    else:
        execute_sql_script()