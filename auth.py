# Пользователи с их API-ключами и ролями
USERS = [
    {"username": "admin", "api_key": "admin_secret_key_123", "role": "admin"},
    {"username": "user", "api_key": "user_readonly_key_456", "role": "user"},
]

def is_valid_api_key(api_key: str) -> bool:
    return any(user["api_key"] == api_key for user in USERS)

def is_admin(api_key: str) -> bool:
    return any(user["api_key"] == api_key and user["role"] == "admin" for user in USERS)

def require_api_key(read_only: bool = True):
    from functools import wraps
    from flask import request, Response
    import json

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Пробуем получить ключ из заголовков или параметров
            api_key = request.headers.get("api_key") or request.args.get("api_key")
            if not api_key:
                return Response(json.dumps({"error": "API-ключ не предоставлен"}, ensure_ascii=False), status=403, mimetype="application/json; charset=utf-8")
            if not is_valid_api_key(api_key):
                return Response(json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False), status=403, mimetype="application/json; charset=utf-8")
            if not read_only and not is_admin(api_key):
                return Response(json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False), status=403, mimetype="application/json; charset=utf-8")
            return fn(*args, **kwargs)
        return wrapper
    return decorator