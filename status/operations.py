from utils.storage import session
from user.models import User

from .models import Status


def set_user(uid):
    user = session.query(User).filter_by(id=uid).first()
    if user is not None:
        status = session.query(Status).all().first()
        status.user_id = uid
        session.commit()


def set_ttp(url):
    status = session.query(Status).all().first()
    status.ttp = url
    session.commit()
