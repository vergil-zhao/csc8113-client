from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.storage import Base


class Status(Base):
    __tablename__ = 'client_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('client_users.id'))
    ttp = Column(String)

    user = relationship('User')

    def __repr__(self):
        return f"<Status ttp='{self.ttp}' user={self.user}>"
