import json
import requests

from utils.storage import session

from .models import User


def all_users():
    return session.query(User).all()


def register_user(user: User):
    data = json.dumps(user.to_dict())
    print(data)
