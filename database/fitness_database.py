import sqlite3
import os
from typing import List, Tuple, Optional

# Константы для путей к файлам
DB_PATH = os.path.join(os.path.dirname(__file__), 'fitness_club.db')
SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql_scripts', 'complete_database.sql')

def read_sql_file(filepath: str) -> str:
    """
    Читает текст SQL-скрипта из файла и возвращает его содержимое.
    
    Args:
        filepath: Путь к SQL файлу
        
    Returns:
        Содержимое SQL файла в виде строки
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {filepath} не найден")
        return ""
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return ""
    
def execute_script(conn, script: str) -> None:
    """
    Принимает соединение и текст скрипта, создаёт курсор, выполняет скрипт 
    через метод executescript, сохраняет изменения.
    
    Args:
        conn: Соединение с базой данных
        script: Текст SQL скрипта
    """
    try:
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        print("SQL скрипт выполнен успешно")
    except Exception as e:
        print(f"Ошибка при выполнении SQL скрипта: {e}")
        conn.rollback()    

def find_appointment_by_phone(conn, phone: str) -> List[Tuple]:
    """
    Принимает соединение и номер телефона, выполняет параметризованный SELECT-запрос 
    на точное совпадение номера телефона, возвращает список найденных записей.
    В записях человекочитаемые имена тренеров и названия тренировок.
    
    Args:
        conn: Соединение с базой данных
        phone: Номер телефона для поиска
        
    Returns:
        Список найденных записей
    """
    try:
        cursor = conn.cursor()
        query = """
        SELECT 
            a.id,
            a.last_name || ' ' || a.first_name as client_name,
            a.phone,
            t.last_name || ' ' || t.first_name || ' ' || t.middle_name as trainer_name,
            a.name_of_training_session,
            a.comment,
            a.status,
            a.appointment_date
        FROM appointments a
        LEFT JOIN trainers t ON a.trener_id = t.id
        WHERE a.phone = ?
        """
        cursor.execute(query, (phone,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при поиске по телефону: {e}")
        return []
    
def find_appointment_by_comment(conn, comment_part: str) -> List[Tuple]:
    """
    Принимает соединение и часть комментария, ищет записи, где комментарий 
    содержит переданную строку, используя оператор LIKE, возвращает список найденных записей.
    В записях человекочитаемые имена тренеров и названия тренировок.
    
    Args:
        conn: Соединение с базой данных
        comment_part: Часть комментария для поиска
        
    Returns:
        Список найденных записей
    """
    try:
        cursor = conn.cursor()
        query = """
        SELECT 
            a.id,
            a.last_name || ' ' || a.first_name as client_name,
            a.phone,
            t.last_name || ' ' || t.first_name || ' ' || t.middle_name as trainer_name,
            a.name_of_training_session,
            a.comment,
            a.status,
            a.appointment_date
        FROM appointments a
        LEFT JOIN trainers t ON a.trener_id = t.id
        WHERE a.comment LIKE ?
        """
        cursor.execute(query, (f'%{comment_part}%',))
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при поиске по комментарию: {e}")
        return []
    
def create_appointment(conn, client_name: str, client_phone: str, trainer_name: str, 
                      workouts_list: List[str], comment: str = None) -> int:
    """
    Создаёт новую запись в таблице клиентов, принимает имя клиента, телефон, 
    имя тренера и список тренировок. Ищет тренера и тренировки по именам, 
    вставляет запись в базу, связывает её с тренировками. Возвращает ID созданной записи.
    
    Args:
        conn: Соединение с базой данных
        client_name: Имя клиента (Фамилия Имя)
        client_phone: Телефон клиента
        trainer_name: Имя тренера (Фамилия Имя Отчество)
        workouts_list: Список названий тренировок
        comment: Комментарий к записи (опционально)
        
    Returns:
        ID созданной записи или -1 при ошибке
    """
    try:
        cursor = conn.cursor()
        
        # Разделяем имя клиента на части
        name_parts = client_name.split()
        if len(name_parts) < 2:
            print("Имя клиента должно содержать фамилию и имя")
            return -1
        
        client_last_name = name_parts[0]
        client_first_name = name_parts[1]
        client_middle_name = name_parts[2] if len(name_parts) > 2 else ""
        
        # Разделяем имя тренера на части
        trainer_parts = trainer_name.split()
        if len(trainer_parts) < 3:
            print("Имя тренера должно содержать фамилию, имя и отчество")
            return -1
        
        trainer_last_name = trainer_parts[0]
        trainer_first_name = trainer_parts[1]
        trainer_middle_name = trainer_parts[2]
        
        # Ищем тренера по имени
        cursor.execute("""
            SELECT id FROM trainers 
            WHERE last_name = ? AND first_name = ? AND middle_name = ?
        """, (trainer_last_name, trainer_first_name, trainer_middle_name))
        
        trainer_result = cursor.fetchone()
        if not trainer_result:
            print(f"Тренер {trainer_name} не найден")
            return -1
        
        trainer_id = trainer_result[0]
        
        # Создаем запись в таблице appointments
        cursor.execute("""
            INSERT INTO appointments (last_name, first_name, phone, trener_id, name_of_training_session, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (client_last_name, client_first_name, client_phone, trainer_id, workouts_list[0], comment or ""))
        
        appointment_id = cursor.lastrowid
        
        # Связываем запись с тренировками
        for workout_name in workouts_list:
            cursor.execute("SELECT id FROM workouts WHERE name_of_training_session = ?", (workout_name,))
            workout_result = cursor.fetchone()
            if workout_result:
                workout_id = workout_result[0]
                cursor.execute("""
                    INSERT INTO appointments_workouts (appointment_id, workout_id)
                    VALUES (?, ?)
                """, (appointment_id, workout_id))
        
        conn.commit()
        print(f"Запись создана с ID: {appointment_id}")
        return appointment_id
        
    except Exception as e:
        print(f"Ошибка при создании записи: {e}")
        conn.rollback()
        return -1
    
if __name__ == "__main__":
    # Создание соединения с базой данных
    conn = sqlite3.connect(DB_PATH)
    
    try:
        print("=" * 60)
        print("ТЕСТИРОВАНИЕ ФУНКЦИЙ РАБОТЫ С БАЗОЙ ДАННЫХ")
        print("=" * 60)
        
        # Тест 1: Чтение SQL файла
        print("\n1. Тест чтения SQL файла:")
        sql_content = read_sql_file(SQL_PATH)
        if sql_content:
            print(f"SQL файл прочитан успешно. Размер: {len(sql_content)} символов")
        else:
            print("Ошибка при чтении SQL файла")
        
        # Тест 2: Поиск записей по телефону
        print("\n2. Тест поиска записей по телефону:")
        phone = "+7(999)123-45-67"
        appointments_by_phone = find_appointment_by_phone(conn, phone)
        print(f"Найдено записей для телефона {phone}: {len(appointments_by_phone)}")
        for appointment in appointments_by_phone:
            print(f"  - ID: {appointment[0]}, Клиент: {appointment[1]}, Тренер: {appointment[3]}, Тренировка: {appointment[4]}")
        
        # Тест 3: Поиск записей по комментарию
        print("\n3. Тест поиска записей по комментарию:")
        comment_part = "йога"
        appointments_by_comment = find_appointment_by_comment(conn, comment_part)
        print(f"Найдено записей с комментарием содержащим '{comment_part}': {len(appointments_by_comment)}")
        for appointment in appointments_by_comment:
            print(f"  - ID: {appointment[0]}, Клиент: {appointment[1]}, Комментарий: {appointment[5]}")
        
        # Тест 4: Создание новой записи
        print("\n4. Тест создания новой записи:")
        new_appointment_id = create_appointment(
            conn=conn,
            client_name="Тестова Анна Петровна",
            client_phone="+7(999)999-99-99",
            trainer_name="Иванов Александр Петрович",
            workouts_list=["Йога для начинающих"],
            comment="Тестовая запись для проверки функции"
        )
        
        if new_appointment_id > 0:
            print(f"Новая запись создана с ID: {new_appointment_id}")
            
            # Проверяем созданную запись
            test_appointments = find_appointment_by_phone(conn, "+7(999)999-99-99")
            print(f"Проверка: найдено записей для нового телефона: {len(test_appointments)}")
            for appointment in test_appointments:
                print(f"  - ID: {appointment[0]}, Клиент: {appointment[1]}, Комментарий: {appointment[5]}")
        else:
            print("Ошибка при создании новой записи")
        
        print("\n" + "=" * 60)
        print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("=" * 60)
        
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
    
    finally:
        # Закрытие соединения
        conn.close()
        print("\nСоединение с базой данных закрыто")