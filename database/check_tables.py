import sqlite3
import os

def check_tables():
    # Путь к файлу базы данных
    db_path = os.path.join(os.path.dirname(__file__), 'fitness_club.db')
    
    # Создание соединения с базой данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Получение списка всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Созданные таблицы:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Проверка структуры каждой таблицы
        for table in tables:
            table_name = table[0]
            print(f"\nСтруктура таблицы '{table_name}':")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'PRIMARY KEY' if col[5] else ''}")
        
    except Exception as e:
        print(f"Ошибка при проверке таблиц: {e}")
    
    finally:
        # Закрытие соединения
        conn.close()

if __name__ == "__main__":
    check_tables()