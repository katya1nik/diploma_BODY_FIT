from flask import Blueprint, request, Response
from models import Trainers
from utils import trainers_to_dict, validate_trainers_data
from auth import require_api_key
import json

trainers_bp = Blueprint("trainers", __name__, url_prefix="/trainers")

@trainers_bp.route("", methods=["GET"])
@require_api_key(read_only=True)
def get_trainers():
    try:
        trainers = Trainers.select()
        data = {"trainers": [trainers_to_dict(t) for t in trainers]}
        return Response(json.dumps(data, ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при получении списка тренеров: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@trainers_bp.route("/<int:trainer_id>", methods=["GET"])
@require_api_key(read_only=True)
def get_trainer(trainer_id: int):
    try:
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        if not trainer:
            return Response(json.dumps({"error": "Тренер не найден"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        return Response(json.dumps(trainers_to_dict(trainer), ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при получении тренера: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@trainers_bp.route("", methods=["POST"])
@require_api_key(read_only=False)
def create_trainer():
    try:
        if not request.json:
            return Response(json.dumps({"error": "Требуются данные в формате JSON"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        data = request.json
        ok, msg = validate_trainers_data(data)
        if not ok:
            return Response(json.dumps({"error": msg}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        trainer = Trainers.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data["middle_name"],
            name_of_training_session=data["name_of_training_session"],
            phone=data.get("phone"),
            email=data.get("email"),
            specialization=data.get("specialization"),
            experience_years=data.get("experience_years", 0),
        )
        return Response(json.dumps(trainers_to_dict(trainer), ensure_ascii=False), status=201, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при создании тренера: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@trainers_bp.route("/<int:trainer_id>", methods=["PUT"])
@require_api_key(read_only=False)
def update_trainer(trainer_id: int):
    try:
        if not request.json:
            return Response(json.dumps({"error": "Требуются данные в формате JSON"}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        if not trainer:
            return Response(json.dumps({"error": "Тренер не найден"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        data = request.json
        ok, msg = validate_trainers_data(data)
        if not ok:
            return Response(json.dumps({"error": msg}, ensure_ascii=False), status=400, mimetype="application/json; charset=utf-8")
        trainer.first_name = data["first_name"]
        trainer.last_name = data["last_name"]
        trainer.middle_name = data["middle_name"]
        trainer.name_of_training_session = data["name_of_training_session"]
        trainer.phone = data.get("phone")
        trainer.email = data.get("email")
        trainer.specialization = data.get("specialization")
        trainer.experience_years = data.get("experience_years", 0)
        trainer.save()
        return Response(json.dumps(trainers_to_dict(trainer), ensure_ascii=False), status=200, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при обновлении тренера: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")

@trainers_bp.route("/<int:trainer_id>", methods=["DELETE"])
@require_api_key(read_only=False)
def delete_trainer(trainer_id: int):
    try:
        trainer = Trainers.get_or_none(Trainers.id == trainer_id)
        if not trainer:
            return Response(json.dumps({"error": "Тренер не найден"}, ensure_ascii=False), status=404, mimetype="application/json; charset=utf-8")
        trainer.delete_instance()
        return Response("", status=204)
    except Exception as e:
        return Response(json.dumps({"error": f"Ошибка при удалении тренера: {e}"}, ensure_ascii=False), status=500, mimetype="application/json; charset=utf-8")