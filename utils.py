from typing import Any, Dict, Tuple
from models import Trainers, Appointments

def trainers_to_dict(trainer: Trainers) -> Dict[str, Any]:
    return {
        "id": trainer.id,
        "first_name": trainer.first_name,
        "middle_name": trainer.middle_name,
        "last_name": trainer.last_name,
        "phone": trainer.phone,
        "email": trainer.email,
        "specialization": trainer.specialization,
        "experience_years": trainer.experience_years,
        "name_of_training_session": trainer.name_of_training_session,
        "created_at": trainer.created_at.isoformat() if trainer.created_at else None,
    }

def appointments_to_dict(appointment: Appointments) -> Dict[str, Any]:
    trainer_info = None
    if appointment.trener:
        trainer_info = {
            "id": appointment.trener.id,
            "first_name": appointment.trener.first_name,
            "last_name": appointment.trener.last_name,
            "middle_name": appointment.trener.middle_name,
        }
    return {
        "id": appointment.id,
        "client_name": f"{appointment.last_name} {appointment.first_name}",
        "client_phone": appointment.phone,
        "date": appointment.date.isoformat() if appointment.date else None,
        "appointment_date": appointment.appointment_date.isoformat() if appointment.appointment_date else None,
        "name_of_training_session": appointment.name_of_training_session,
        "comment": appointment.comment,
        "trainer": trainer_info,
        "created_at": appointment.created_at.isoformat() if appointment.created_at else None,
    }

def validate_trainers_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    required_fields = ["first_name", "last_name", "middle_name", "name_of_training_session"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Поле '{field}' обязательно для заполнения"
    if len(data["first_name"]) > 100 or len(data["last_name"]) > 100 or len(data["middle_name"]) > 100:
        return False, "Имя/Фамилия/Отчество не должны превышать 100 символов"
    if len(data["name_of_training_session"]) > 200:
        return False, "Название тренировки не должно превышать 200 символов"
    if data.get("phone") and len(data["phone"]) > 20:
        return False, "Телефон не должен превышать 20 символов"
    if data.get("email") and len(data["email"]) > 100:
        return False, "Email не должен превышать 100 символов"
    return True, ""

def validate_appointments_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    required_fields = ["first_name", "last_name", "phone", "name_of_training_session"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Поле '{field}' обязательно для заполнения"
    if len(data["first_name"]) > 100 or len(data["last_name"]) > 100:
        return False, "Имя/Фамилия не должны превышать 100 символов"
    if len(data["phone"]) > 20:
        return False, "Телефон не должен превышать 20 символов"
    if len(data["name_of_training_session"]) > 200:
        return False, "Название тренировки не должно превышать 200 символов"
    return True, ""