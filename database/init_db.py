import sqlite3
import os

def create_database():
    # Путь к файлу базы данных
    db_path = os.path.join(os.path.dirname(__file__), 'fitness_club.db')
    
    # Создание соединения с базой данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("База данных создана успешно!")
    print(f"Путь: {db_path}")
    
    # Закрытие соединения
    conn.close()

if __name__ == "__main__":
    create_database()