from random import randint
from fastapi import HTTPException


def generate_verification_code():
    try:
        code = randint(1000000, 9999999)
        return code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

