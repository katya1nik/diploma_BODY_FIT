import sqlite3
import os

def check_data():
    # Путь к файлу базы данных
    db_path = os.path.join(os.path.dirname(__file__), 'fitness_club.db')
    
    # Создание соединения с базой данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Проверка количества записей в каждой таблице
        tables = ['trainers', 'workouts', 'clients', 'appointments', 'trainers_workouts', 'appointments_workouts']
        
        print("Количество записей в таблицах:")
        print("="*40)
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"Таблица {table}: {count} записей")
        
        print("\n" + "="*50)
        
        # Показать несколько примеров данных
        print("\nПримеры тренеров:")
        cursor.execute("SELECT last_name, first_name, middle_name, name_of_training_session FROM trainers LIMIT 5;")
        for row in cursor.fetchall():
            print(f"  {row[0]} {row[1]} {row[2]} - {row[3]}")
        
        print("\nПримеры тренировок:")
        cursor.execute("SELECT name_of_training_session, last_name, first_name, description FROM workouts LIMIT 5;")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]} {row[2]} - {row[3]}")
        
        print("\nПримеры клиентов:")
        cursor.execute("SELECT last_name, first_name, middle_name, phone FROM clients LIMIT 5;")
        for row in cursor.fetchall():
            print(f"  {row[0]} {row[1]} {row[2]} - {row[3]}")
        
        print("\nПримеры записей:")
        cursor.execute("SELECT last_name, first_name, phone, name_of_training_session FROM appointments LIMIT 5;")
        for row in cursor.fetchall():
            print(f"  {row[0]} {row[1]} - {row[2]} - {row[3]}")
        
        print("\nПримеры связей тренеров и тренировок:")
        cursor.execute("SELECT t.last_name, t.first_name, w.name_of_training_session FROM trainers t JOIN trainers_workouts tw ON t.id = tw.trener_id JOIN workouts w ON tw.workout_id = w.id LIMIT 5;")
        for row in cursor.fetchall():
            print(f"  {row[0]} {row[1]} ведет {row[2]}")
        
    except Exception as e:
        print(f"Ошибка при проверке данных: {e}")
    
    finally:
        # Закрытие соединения
        conn.close()

if __name__ == "__main__":
    check_data()