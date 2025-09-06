from flask import Flask, request, json
from peewee import *
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

# Инициализация Flask приложения
app = Flask(__name__)

# Настройка базы данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'BODY_FIT.db')
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

class Appointments(BaseModel):
    """Модель записей на тренировки"""
    last_name = CharField(max_length=100, null=False)
    first_name = CharField(max_length=100, null=False)
    phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    trener = ForeignKeyField(Trainers, backref='appointments', null=True, on_delete='SET NULL')
    name_of_training_session = CharField(max_length=200, null=False)
    comment = TextField(null=True)
    appointment_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)

# =====================================================
# ФУНКЦИИ-ПОМОЩНИКИ
# =====================================================

def trainers_to_dict(trainer: Trainers) -> Dict[str, Any]:
    """
    Преобразует объект Trainers в словарь
    
    Args:
        trainer: Объект тренера
        
    Returns:
        Словарь с данными тренера
    """
    return {
        'id': trainer.id,
        'first_name': trainer.first_name,
        'middle_name': trainer.middle_name,
        'last_name': trainer.last_name,
        'phone': trainer.phone,
        'email': trainer.email,
        'specialization': trainer.specialization,
        'experience_years': trainer.experience_years,
        'name_of_training_session': trainer.name_of_training_session,
        'created_at': trainer.created_at.isoformat() if trainer.created_at else None
    }

def appointments_to_dict(appointment: Appointments) -> Dict[str, Any]:
    """
    Преобразует объект Appointments в словарь с включением информации о тренере
    
    Args:
        appointment: Объект записи
        
    Returns:
        Словарь с данными записи и тренера
    """
    trainer_info = None
    if appointment.trener:
        trainer_info = {
            'id': appointment.trener.id,
            'first_name': appointment.trener.first_name,
            'last_name': appointment.trener.last_name,
            'middle_name': appointment.trener.middle_name
        }
    
    return {
        'id': appointment.id,
        'client_name': f"{appointment.last_name} {appointment.first_name}",
        'client_phone': appointment.phone,
        'date': appointment.date.isoformat() if appointment.date else None,
        'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
        'name_of_training_session': appointment.name_of_training_session,
        'comment': appointment.comment,
        'trainer': trainer_info,
        'created_at': appointment.created_at.isoformat() if appointment.created_at else None
    }

def validate_trainers_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Проверяет корректность данных для создания/обновления тренера
    
    Args:
        data: Словарь с данными тренера
        
    Returns:
        Кортеж (валидность, сообщение об ошибке)
    """
    required_fields = ['first_name', 'last_name', 'middle_name', 'name_of_training_session']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Поле '{field}' обязательно для заполнения"
    
    # Проверка длины полей
    if len(data['first_name']) > 100:
        return False, "Имя не должно превышать 100 символов"
    if len(data['last_name']) > 100:
        return False, "Фамилия не должна превышать 100 символов"
    if len(data['middle_name']) > 100:
        return False, "Отчество не должно превышать 100 символов"
    if len(data['name_of_training_session']) > 200:
        return False, "Название тренировки не должно превышать 200 символов"
    
    # Проверка телефона (если указан)
    if 'phone' in data and data['phone'] and len(data['phone']) > 20:
        return False, "Телефон не должен превышать 20 символов"
    
    # Проверка email (если указан)
    if 'email' in data and data['email'] and len(data['email']) > 100:
        return False, "Email не должен превышать 100 символов"
    
    return True, ""

def validate_appointments_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Проверяет корректность данных для создания/обновления записи
    
    Args:
        data: Словарь с данными записи
        
    Returns:
        Кортеж (валидность, сообщение об ошибке)
    """
    required_fields = ['first_name', 'last_name', 'phone', 'name_of_training_session']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Поле '{field}' обязательно для заполнения"
    
    # Проверка длины полей
    if len(data['first_name']) > 100:
        return False, "Имя не должно превышать 100 символов"
    if len(data['last_name']) > 100:
        return False, "Фамилия не должна превышать 100 символов"
    if len(data['phone']) > 20:
        return False, "Телефон не должен превышать 20 символов"
    if len(data['name_of_training_session']) > 200:
        return False, "Название тренировки не должно превышать 200 символов"
    
    # Проверка существования тренера (если указан)
    if 'trainer_id' in data and data['trainer_id']:
        try:
            trainer_id = int(data['trainer_id'])
            if not Trainers.select().where(Trainers.id == trainer_id).exists():
                return False, "Тренер с указанным ID не найден"
        except (ValueError, TypeError):
            return False, "ID тренера должен быть числом"
    
    return True, ""

# =====================================================
# МАРШРУТЫ ДЛЯ ТРЕНЕРОВ
# =====================================================

@app.route('/trainers', methods=['GET'])
def get_trainers():
    """Получить список всех тренеров"""
    try:
        trainers = Trainers.select()
        trainers_data = [trainers_to_dict(trainer) for trainer in trainers]
        
        response_data = {'trainers': trainers_data}
        return json.dumps(response_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при получении списка тренеров: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trainers/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    """Получить информацию о тренере по ID"""
    try:
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        
        if not trainer:
            error_data = {'error': 'Тренер не найден'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        trainer_data = trainers_to_dict(trainer)
        return json.dumps(trainer_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при получении тренера: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trainers', methods=['POST'])
def create_trainer():
    """Добавить нового тренера"""
    try:
        if not request.json:
            error_data = {'error': 'Требуются данные в формате JSON'}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        data = request.json
        
        # Валидация данных
        is_valid, error_message = validate_trainers_data(data)
        if not is_valid:
            error_data = {'error': error_message}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Создание тренера
        trainer = Trainers.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data['middle_name'],
            name_of_training_session=data['name_of_training_session'],
            phone=data.get('phone'),
            email=data.get('email'),
            specialization=data.get('specialization'),
            experience_years=data.get('experience_years', 0)
        )
        
        trainer_data = trainers_to_dict(trainer)
        return json.dumps(trainer_data, ensure_ascii=False), 201, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при создании тренера: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trainers/<int:trainer_id>', methods=['PUT'])
def update_trainer(trainer_id):
    """Обновить информацию о тренере"""
    try:
        if not request.json:
            error_data = {'error': 'Требуются данные в формате JSON'}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        data = request.json
        
        # Проверка существования тренера
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        if not trainer:
            error_data = {'error': 'Тренер не найден'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Валидация данных
        is_valid, error_message = validate_trainers_data(data)
        if not is_valid:
            error_data = {'error': error_message}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Обновление тренера
        trainer.first_name = data['first_name']
        trainer.last_name = data['last_name']
        trainer.middle_name = data['middle_name']
        trainer.name_of_training_session = data['name_of_training_session']
        trainer.phone = data.get('phone')
        trainer.email = data.get('email')
        trainer.specialization = data.get('specialization')
        trainer.experience_years = data.get('experience_years', 0)
        trainer.save()
        
        trainer_data = trainers_to_dict(trainer)
        return json.dumps(trainer_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при обновлении тренера: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trainers/<int:trainer_id>', methods=['DELETE'])
def delete_trainer(trainer_id):
    """Удалить тренера"""
    try:
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        
        if not trainer:
            error_data = {'error': 'Тренер не найден'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        trainer.delete_instance()
        return '', 204
    
    except Exception as e:
        error_data = {'error': f'Ошибка при удалении тренера: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

# =====================================================
# МАРШРУТЫ ДЛЯ ЗАПИСЕЙ НА ТРЕНИРОВКИ
# =====================================================

@app.route('/appointments', methods=['GET'])
def get_appointments():
    """Получить все записи на тренировки с опциональной сортировкой"""
    try:
        # Получение параметров сортировки
        sort_by = request.args.get('sort_by', 'created_at')
        direction = request.args.get('direction', 'asc')
        
        # Валидация поля сортировки
        valid_sort_fields = ['id', 'last_name', 'first_name', 'phone', 'date', 'appointment_date', 'status', 'created_at']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        # Построение запроса с сортировкой
        query = Appointments.select()
        
        if sort_by == 'last_name':
            if direction == 'desc':
                query = query.order_by(Appointments.last_name.desc())
            else:
                query = query.order_by(Appointments.last_name)
        elif sort_by == 'first_name':
            if direction == 'desc':
                query = query.order_by(Appointments.first_name.desc())
            else:
                query = query.order_by(Appointments.first_name)
        elif sort_by == 'phone':
            if direction == 'desc':
                query = query.order_by(Appointments.phone.desc())
            else:
                query = query.order_by(Appointments.phone)
        elif sort_by == 'date':
            if direction == 'desc':
                query = query.order_by(Appointments.date.desc())
            else:
                query = query.order_by(Appointments.date)
        elif sort_by == 'appointment_date':
            if direction == 'desc':
                query = query.order_by(Appointments.appointment_date.desc())
            else:
                query = query.order_by(Appointments.appointment_date)
        elif sort_by == 'status':
            if direction == 'desc':
                query = query.order_by(Appointments.status.desc())
            else:
                query = query.order_by(Appointments.status)
        elif sort_by == 'created_at':
            if direction == 'desc':
                query = query.order_by(Appointments.created_at.desc())
            else:
                query = query.order_by(Appointments.created_at)
        else:  # id
            if direction == 'desc':
                query = query.order_by(Appointments.id.desc())
            else:
                query = query.order_by(Appointments.id)
        
        appointments = query
        appointments_data = [appointments_to_dict(appointment) for appointment in appointments]
        
        response_data = {'appointments': appointments_data}
        return json.dumps(response_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при получении записей: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Получить запись по ID"""
    try:
        appointment = Appointments.get_or_none(Appointments.id == appointment_id)
        
        if not appointment:
            error_data = {'error': 'Запись не найдена'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        appointment_data = appointments_to_dict(appointment)
        response_data = {'appointment': appointment_data}
        return json.dumps(response_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при получении записи: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/appointments/trainers/<int:trainer_id>', methods=['GET'])
def get_appointments_by_trainer(trainer_id):
    """Получить все записи для заданного тренера"""
    try:
        # Проверка существования тренера
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        if not trainer:
            error_data = {'error': 'Тренер не найден'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        appointments = Appointments.select().where(Appointments.trener == trainer_id)
        appointments_data = [appointments_to_dict(appointment) for appointment in appointments]
        
        response_data = {'appointments': appointments_data}
        return json.dumps(response_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при получении записей тренера: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/appointments', methods=['POST'])
def create_appointment():
    """Создать новую запись"""
    try:
        if not request.json:
            error_data = {'error': 'Требуются данные в формате JSON'}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        data = request.json
        
        # Валидация данных
        is_valid, error_message = validate_appointments_data(data)
        if not is_valid:
            error_data = {'error': error_message}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Получение тренера (если указан)
        trainer = None
        if 'trainer_id' in data and data['trainer_id']:
            trainer = Trainers.get_or_none(Trainers.id == data['trainer_id'])
            if not trainer:
                error_data = {'error': 'Тренер с указанным ID не найден'}
                return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Создание записи
        appointment = Appointments.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            name_of_training_session=data['name_of_training_session'],
            trener=trainer,
            comment=data.get('comment'),
            appointment_date=data.get('appointment_date')
        )
        
        appointment_data = appointments_to_dict(appointment)
        return json.dumps(appointment_data, ensure_ascii=False), 201, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при создании записи: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Обновить запись"""
    try:
        if not request.json:
            error_data = {'error': 'Требуются данные в формате JSON'}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        data = request.json
        
        # Проверка существования записи
        appointment = Appointments.get_or_none(Appointments.id == appointment_id)
        if not appointment:
            error_data = {'error': 'Запись не найдена'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Валидация данных
        is_valid, error_message = validate_appointments_data(data)
        if not is_valid:
            error_data = {'error': error_message}
            return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Получение тренера (если указан)
        trainer = None
        if 'trainer_id' in data and data['trainer_id']:
            trainer = Trainers.get_or_none(Trainers.id == data['trainer_id'])
            if not trainer:
                error_data = {'error': 'Тренер с указанным ID не найден'}
                return json.dumps(error_data, ensure_ascii=False), 400, {'Content-Type': 'application/json; charset=utf-8'}
        
        # Обновление записи
        appointment.first_name = data['first_name']
        appointment.last_name = data['last_name']
        appointment.phone = data['phone']
        appointment.name_of_training_session = data['name_of_training_session']
        appointment.trener = trainer
        appointment.comment = data.get('comment')
        appointment.status = data.get('status', 'Запланировано')
        appointment.appointment_date = data.get('appointment_date')
        appointment.save()
        
        appointment_data = appointments_to_dict(appointment)
        return json.dumps(appointment_data, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        error_data = {'error': f'Ошибка при обновлении записи: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Удалить запись"""
    try:
        appointment = Appointments.get_or_none(Appointments.id == appointment_id)
        
        if not appointment:
            error_data = {'error': 'Запись не найдена'}
            return json.dumps(error_data, ensure_ascii=False), 404, {'Content-Type': 'application/json; charset=utf-8'}
        
        appointment.delete_instance()
        return '', 204
    
    except Exception as e:
        error_data = {'error': f'Ошибка при удалении записи: {str(e)}'}
        return json.dumps(error_data, ensure_ascii=False), 500, {'Content-Type': 'application/json; charset=utf-8'}

# =====================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# =====================================================

if __name__ == '__main__':
    # Создание таблиц, если они не существуют
    DB.connect()
    DB.create_tables([Trainers, Appointments], safe=True)
    DB.close()
    
    # Запуск веб-сервера
    app.run(debug=True)