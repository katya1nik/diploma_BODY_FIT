from flask import Blueprint, request, Response
from models import Appointments, Trainers
from utils import appointments_to_dict, validate_appointments_data
from auth import require_api_key
import json

appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")

@appointments_bp.route("", methods=["GET"])
@require_api_key(read_only=True)
def get_appointments():
    try:
        sort_by = request.args.get("sort_by", "created_at")
        direction = request.args.get("direction", "asc")
        valid = {"id", "last_name", "first_name", "phone", "date", "appointment_date", "created_at"}
        if sort_by not in valid:
            sort_by = "created_at"
        field = getattr(Appointments, sort_by)
        query = Appointments.select().order_by(field.desc() if direction == "desc" else field)
        data = {"appointments": [appointments_to_dict(a) for a in query]}
        return Response(json.dumps(data, ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при получении записей: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@appointments_bp.route("/<int:appointment_id>", methods=["GET"])
@require_api_key(read_only=True)
def get_appointment(appointment_id: int):
    try:
        a = Appointments.get_or_none(Appointments.id == appointment_id)
        if not a:
            return Response(json.dumps({"error": "Запись не найдена"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        return Response(json.dumps({"appointment": appointments_to_dict(a)}, ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при получении записи: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@appointments_bp.route("/trainers/<int:trainer_id>", methods=["GET"])
@require_api_key(read_only=True)
def get_appointments_by_trainer(trainer_id: int):
    try:
        if not Trainers.select().where(Trainers.id == trainer_id).exists():
            return Response(json.dumps({"error": "Тренер не найден"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        query = Appointments.select().where(Appointments.trener == trainer_id)
        data = {"appointments": [appointments_to_dict(a) for a in query]}
        return Response(json.dumps(data, ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при получении записей тренера: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@appointments_bp.route("", methods=["POST"])
@require_api_key(read_only=False)
def create_appointment():
    try:
        if not request.json:
            return Response(json.dumps({"error": "Требуются данные в формате JSON"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        data = request.json
        ok, msg = validate_appointments_data(data)
        if not ok:
            return Response(json.dumps({"error": msg}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        trainer = None
        if data.get("trainer_id"):
            trainer = Trainers.get_or_none(Trainers.id == data["trainer_id"])
            if not trainer:
                return Response(json.dumps({"error": "Тренер с указанным ID не найден"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        a = Appointments.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            name_of_training_session=data["name_of_training_session"],
            trener=trainer,
            comment=data.get("comment"),
            appointment_date=data.get("appointment_date"),
        )
        return Response(json.dumps(appointments_to_dict(a), ensure_ascii=False), status=201, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при создании записи: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@appointments_bp.route("/<int:appointment_id>", methods=["PUT"])
@require_api_key(read_only=False)
def update_appointment(appointment_id: int):
    try:
        if not request.json:
            return Response(json.dumps({"error": "Требуются данные в формате JSON"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        a = Appointments.get_or_none(Appointments.id == appointment_id)
        if not a:
            return Response(json.dumps({"error": "Запись не найдена"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        data = request.json
        ok, msg = validate_appointments_data(data)
        if not ok:
            return Response(json.dumps({"error": msg}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        trainer = None
        if data.get("trainer_id"):
            trainer = Trainers.get_or_none(Trainers.id == data["trainer_id"])
            if not trainer:
                return Response(json.dumps({"error": "Тренер с указанным ID не найден"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        a.first_name = data["first_name"]
        a.last_name = data["last_name"]
        a.phone = data["phone"]
        a.name_of_training_session = data["name_of_training_session"]
        a.trener = trainer
        a.comment = data.get("comment")
        a.appointment_date = data.get("appointment_date")
        a.save()
        return Response(json.dumps(appointments_to_dict(a), ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при обновлении записи: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@appointments_bp.route("/<int:appointment_id>", methods=["DELETE"])
@require_api_key(read_only=False)
def delete_appointment(appointment_id: int):
    try:
        a = Appointments.get_or_none(Appointments.id == appointment_id)
        if not a:
            return Response(json.dumps({"error": "Запись не найдена"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        a.delete_instance()
        return Response("", status=204)
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при удалении записи: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")