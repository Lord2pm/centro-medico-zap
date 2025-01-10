from django.shortcuts import HttpResponse

from .models import User


def register_user(username: str, phone: str) -> bool:
    user = User(nome=username, telefone=phone)
    try:
        user.save()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_by_phone(phone) -> User:
    user = User.objects.get(telefone=phone)
    return user
