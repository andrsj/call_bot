from sqlalchemy import Column, Integer, String
from .database import Base


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(12))

    def __init__(self, phone, name):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return f"< Phone ( {self.phone} {self.name} ) >"
