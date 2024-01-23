from fastapi import Request, Response


def user_cache_key_builder(func, namespace: str, request: Request, response: Response, args, kwargs):
    # Получение текущего пользователя из зависимостей
    current_user = kwargs["current_user"]
    user_id = current_user.id
    # Создание ключа кэша с ID пользователя
    return f"{user_id}"