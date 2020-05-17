from sqlalchemy import Column, Integer, String, Boolean
from textwrap import dedent


from .database import Base


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    phone = Column(String(12), unique=True)
    priority = Column(Boolean)
    banned = Column(Boolean)

    def __init__(self, phone, name, priority=False, banned=False):
        self.name = name
        self.phone = phone
        self.priority = priority
        self.banned = banned

    def __repr__(self):
        return dedent(f"""
        < Phone ( {self.phone}, {self.name} ) >
        [User banned:{self.banned}, priority:{self.priority}]""")
