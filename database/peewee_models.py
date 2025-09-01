from peewee import *
import os
from datetime import datetime
from typing import List, Optional

# Создание базы данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'BODY_FIT.db')
DB = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    """Базовая модель для всех таблиц"""
    class Meta:
        database = DB

class Trainers(BaseModel):
    """Модель тренеров"""
    last_name = CharField(max_length=100, null=False)
    first_name = CharField(max_length=100, null=False)
    middle_name = CharField(max_length=100, null=False)
    name_of_training_session = CharField(max_length=200, null=False)
    phone = CharField(max_length=20, null=True)
    email = CharField(max_length=100, null=True)
    specialization = CharField(max_length=200, null=True)
    experience_years = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.now)

class Workouts(BaseModel):
    """Модель тренировок"""
    name_of_training_session = CharField(max_length=200, null=False)
    last_name = CharField(max_length=100, null=False)
    first_name = CharField(max_length=100, null=False)
    middle_name = CharField(max_length=100, null=False)
    description = TextField(null=True)
    duration_minutes = IntegerField(default=60)
    max_participants = IntegerField(default=10)
    difficulty_level = CharField(max_length=20, null=True, 
                               choices=[('Начинающий', 'Начинающий'), 
                                      ('Средний', 'Средний'), 
                                      ('Продвинутый', 'Продвинутый')])
    created_at = DateTimeField(default=datetime.now)

class Clients(BaseModel):
    """Модель клиентов"""
    last_name = CharField(max_length=100, null=False)
    first_name = CharField(max_length=100, null=False)
    middle_name = CharField(max_length=100, null=False)
    phone = CharField(max_length=20, null=False, unique=True)
    name_of_training_session = CharField(max_length=200, null=False)
    email = CharField(max_length=100, null=True)
    birth_date = DateField(null=True)
    membership_type = CharField(max_length=20, null=True,
                              choices=[('Разовый', 'Разовый'), 
                                     ('Месячный', 'Месячный'), 
                                     ('Годовой', 'Годовой')])
    registration_date = DateTimeField(default=datetime.now)

class Appointments(BaseModel):
    """Модель записей на тренировки"""
    last_name = CharField(max_length=100, null=False)
    first_name = CharField(max_length=100, null=False)
    phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    trener = ForeignKeyField(Trainers, backref='appointments', null=True, on_delete='SET NULL')
    name_of_training_session = CharField(max_length=200, null=False)
    comment = TextField(null=True)
    status = CharField(max_length=20, default='Запланировано',
                     choices=[('Запланировано', 'Запланировано'), 
                             ('Проведено', 'Проведено'), 
                             ('Отменено', 'Отменено')])
    appointment_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)

class TrainersWorkouts(BaseModel):
    """Связующая таблица тренеров и тренировок (многие ко многим)"""
    trainer = ForeignKeyField(Trainers, backref='trainer_workouts', on_delete='CASCADE')
    workout = ForeignKeyField(Workouts, backref='trainer_workouts', on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('trainer', 'workout')

class AppointmentsWorkouts(BaseModel):
    """Связующая таблица записей и тренировок (многие ко многим)"""
    appointment = ForeignKeyField(Appointments, backref='appointment_workouts', on_delete='CASCADE')
    workout = ForeignKeyField(Workouts, backref='appointment_workouts', on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('appointment', 'workout')
        