from sqlalchemy import Column, Integer, String, DateTime
from utils.storage import Base
from utils.signing import Key


class User(Base):
    __tablename__ = 'client_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True)
    name = Column(String)
    public_key = Column(String)
    private_key = Column(String)
    date_registered = Column(DateTime)

    def to_dict(self):
        key = Key(private_key=self.private_key)
        return {
            'name': self.name,
            'public_key': self.public_key,
            'signature': key.sign(self.name.encode('utf8'))
        }

    def __repr__(self):
        return "<User id=%d name='%s' user_id='%s' registered='%s' public_key='%s'>" \
            % (
                   self.id,
                   self.name,
                   self.user_id,
                   self.date_registered,
                   self.public_key
               )
