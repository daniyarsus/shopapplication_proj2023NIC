from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ExceptionHandler:
    """
    Информационные ответы.
    """
    @staticmethod
    async def continue_request():
        return JSONResponse(content={"message": "Continue"}, status_code=100)

    @staticmethod
    async def switching_protocols():
        return JSONResponse(content={"message": "Switching Protocols"}, status_code=101)

    """
    Успешные ответы.
    """
    @staticmethod
    async def ok_response():
        return JSONResponse(content={"message": "OK"}, status_code=200)

    @staticmethod
    async def created_response():
        return JSONResponse(content={"message": "Created"}, status_code=201)

    @staticmethod
    async def no_content_response():
        return JSONResponse(content=None, status_code=204)

    """
    Перенаправления.
    """
    @staticmethod
    async def moved_permanently():
        return JSONResponse(content={"message": "Moved Permanently"}, status_code=301)

    @staticmethod
    async def found():
        return JSONResponse(content={"message": "Found"}, status_code=302)

    @staticmethod
    async def not_modified():
        return JSONResponse(content=None, status_code=304)

    """
    Ошибки клиента.
    """
    @staticmethod
    async def bad_request():
        raise HTTPException(status_code=400, detail="Bad Request")

    @staticmethod
    async def unauthorized():
        raise HTTPException(status_code=401, detail="Unauthorized")

    @staticmethod
    async def not_found():
        raise HTTPException(status_code=404, detail="Not Found")

    @staticmethod
    async def forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")

    """
    Ошибки сервера.
    """
    @staticmethod
    async def internal_server_error():
        raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    async def bad_gateway():
        raise HTTPException(status_code=502, detail="Bad Gateway")

    @staticmethod
    async def service_unavailable():
        raise HTTPException(status_code=503, detail="Service Unavailable")
