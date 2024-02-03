async def info_about_me(current_user):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "username": current_user.username,
        "phone_number": current_user.phone_number,
        "image_bs64": current_user.image_bs64,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }
