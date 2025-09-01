from peewee import *
from peewee_models import *
from datetime import datetime, date
from typing import List

def create_database_and_tables():
    """Создание базы данных и таблиц"""
    try:
        DB.connect()
        DB.create_tables([Trainers, Workouts, Clients, Appointments, TrainersWorkouts, AppointmentsWorkouts])
        print("База данных и таблицы созданы успешно!")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        DB.close()

def insert_test_data():
    """Вставка тестовых данных"""
    try:
        DB.connect()
        
        # Очистка существующих данных
        AppointmentsWorkouts.delete().execute()
        TrainersWorkouts.delete().execute()
        Appointments.delete().execute()
        Clients.delete().execute()
        Workouts.delete().execute()
        Trainers.delete().execute()
        
        print("Существующие данные очищены.")
        
        # Создание тренеров
        trainer1 = Trainers.create(
            last_name="Иванов",
            first_name="Александр",
            middle_name="Петрович",
            name_of_training_session="Йога",
            phone="+7(999)111-11-11",
            email="ivanov@fitness.ru",
            specialization="Йога и медитация",
            experience_years=5
        )
        
        trainer2 = Trainers.create(
            last_name="Петрова",
            first_name="Мария",
            middle_name="Сергеевна",
            name_of_training_session="Пилатес",
            phone="+7(999)222-22-22",
            email="petrova@fitness.ru",
            specialization="Пилатес и растяжка",
            experience_years=3
        )
        
        trainer3 = Trainers.create(
            last_name="Сидоров",
            first_name="Дмитрий",
            middle_name="Александрович",
            name_of_training_session="Кроссфит",
            phone="+7(999)333-33-33",
            email="sidorov@fitness.ru",
            specialization="Кроссфит и функциональный тренинг",
            experience_years=7
        )
        
        print("Тренеры созданы успешно!")
        
        # Создание тренировок
        workout1 = Workouts.create(
            name_of_training_session="Йога для начинающих",
            last_name="Иванов",
            first_name="Александр",
            middle_name="Петрович",
            description="Мягкая практика для новичков",
            duration_minutes=60,
            max_participants=15,
            difficulty_level="Начинающий"
        )
        
        workout2 = Workouts.create(
            name_of_training_session="Пилатес",
            last_name="Петрова",
            first_name="Мария",
            middle_name="Сергеевна",
            description="Укрепление мышц кора",
            duration_minutes=45,
            max_participants=12,
            difficulty_level="Средний"
        )
        
        workout3 = Workouts.create(
            name_of_training_session="Кроссфит",
            last_name="Сидоров",
            first_name="Дмитрий",
            middle_name="Александрович",
            description="Высокоинтенсивные тренировки",
            duration_minutes=60,
            max_participants=10,
            difficulty_level="Продвинутый"
        )
        
        workout4 = Workouts.create(
            name_of_training_session="Стретчинг",
            last_name="Козлова",
            first_name="Елена",
            middle_name="Владимировна",
            description="Растяжка и гибкость",
            duration_minutes=45,
            max_participants=20,
            difficulty_level="Начинающий"
        )
        
        print("Тренировки созданы успешно!")
        
        # Связывание тренеров и тренировок
        TrainersWorkouts.create(trainer=trainer1, workout=workout1)
        TrainersWorkouts.create(trainer=trainer2, workout=workout2)
        TrainersWorkouts.create(trainer=trainer3, workout=workout3)
        TrainersWorkouts.create(trainer=trainer1, workout=workout4)  # Иванов ведет и йогу, и стретчинг
        
        print("Связи тренеров и тренировок созданы!")
        
        # Создание записей на тренировки
        appointment1 = Appointments.create(
            last_name="Смирнова",
            first_name="Анна",
            phone="+7(999)123-45-67",
            trener=trainer1,
            name_of_training_session="Йога для начинающих",
            comment="Первый раз на йоге, нужна помощь",
            status="Запланировано",
            appointment_date=datetime(2024, 9, 1, 10, 0)
        )
        
        appointment2 = Appointments.create(
            last_name="Петров",
            first_name="Иван",
            phone="+7(999)234-56-78",
            trener=trainer2,
            name_of_training_session="Пилатес",
            comment="Регулярные занятия",
            status="Запланировано",
            appointment_date=datetime(2024, 9, 2, 18, 0)
        )
        
        appointment3 = Appointments.create(
            last_name="Козлов",
            first_name="Петр",
            phone="+7(999)345-67-89",
            trener=trainer3,
            name_of_training_session="Кроссфит",
            comment="Интенсивная тренировка",
            status="Проведено",
            appointment_date=datetime(2024, 8, 30, 19, 0)
        )
        
        print("Записи на тренировки созданы!")
        
        # Связывание записей и тренировок (каждая запись привязана к 2 тренировкам)
        AppointmentsWorkouts.create(appointment=appointment1, workout=workout1)
        AppointmentsWorkouts.create(appointment=appointment1, workout=workout4)
        
        AppointmentsWorkouts.create(appointment=appointment2, workout=workout2)
        AppointmentsWorkouts.create(appointment=appointment2, workout=workout4)
        
        AppointmentsWorkouts.create(appointment=appointment3, workout=workout3)
        AppointmentsWorkouts.create(appointment=appointment3, workout=workout1)
        
        print("Связи записей и тренировок созданы!")
        
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        DB.close()

def display_results():
    """Вывод результатов в консоль"""
    try:
        DB.connect()
        
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТЫ РАБОТЫ С БАЗОЙ ДАННЫХ")
        print("="*60)
        
        # Вывод тренеров
        print("\n1. СПИСОК ТРЕНЕРОВ:")
        print("-" * 40)
        for trainer in Trainers.select():
            print(f"ID: {trainer.id}")
            print(f"Имя: {trainer.last_name} {trainer.first_name} {trainer.middle_name}")
            print(f"Специализация: {trainer.specialization}")
            print(f"Опыт: {trainer.experience_years} лет")
            print(f"Телефон: {trainer.phone}")
            print(f"Email: {trainer.email}")
            print("-" * 20)
        
        # Вывод тренировок
        print("\n2. СПИСОК ТРЕНИРОВОК:")
        print("-" * 40)
        for workout in Workouts.select():
            print(f"ID: {workout.id}")
            print(f"Название: {workout.name_of_training_session}")
            print(f"Описание: {workout.description}")
            print(f"Длительность: {workout.duration_minutes} минут")
            print(f"Максимум участников: {workout.max_participants}")
            print(f"Уровень сложности: {workout.difficulty_level}")
            print("-" * 20)
        
        # Вывод записей с связанными тренировками
        print("\n3. СПИСОК ЗАПИСЕЙ НА ТРЕНИРОВКИ:")
        print("-" * 40)
        for appointment in Appointments.select():
            print(f"ID записи: {appointment.id}")
            print(f"Клиент: {appointment.last_name} {appointment.first_name}")
            print(f"Телефон: {appointment.phone}")
            print(f"Тренер: {appointment.trener.last_name} {appointment.trener.first_name} {appointment.trener.middle_name}")
            print(f"Статус: {appointment.status}")
            print(f"Комментарий: {appointment.comment}")
            
            # Получение связанных тренировок
            related_workouts = (Workouts
                              .select()
                              .join(AppointmentsWorkouts)
                              .where(AppointmentsWorkouts.appointment == appointment))
            
            print("Связанные тренировки:")
            for workout in related_workouts:
                print(f"  - {workout.name_of_training_session} ({workout.difficulty_level})")
            print("-" * 20)
        
        # Статистика
        print("\n4. СТАТИСТИКА:")
        print("-" * 40)
        print(f"Количество тренеров: {Trainers.select().count()}")
        print(f"Количество тренировок: {Workouts.select().count()}")
        print(f"Количество записей: {Appointments.select().count()}")
        print(f"Количество связей тренер-тренировка: {TrainersWorkouts.select().count()}")
        print(f"Количество связей запись-тренировка: {AppointmentsWorkouts.select().count()}")
        
    except Exception as e:
        print(f"Ошибка при выводе результатов: {e}")
    finally:
        DB.close()

if __name__ == "__main__":
    print("Создание базы данных и таблиц...")
    create_database_and_tables()
    
    print("\nВставка тестовых данных...")
    insert_test_data()
    
    print("\nВывод результатов...")
    display_results()
    
    print("\nРабота завершена!")
    