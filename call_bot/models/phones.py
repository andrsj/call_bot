from sqlalchemy import Column, Integer, String, Boolean


from call_bot.models.database import Base


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    phone = Column(String(12), unique=True)
    priority = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)

    def __init__(self, phone, name, priority=False, banned=False):
        self.name = name
        self.phone = phone
        self.priority = priority
        self.banned = banned

    def __repr__(self):
        return (
            f"< Phone ( {self.phone}, {self.name} ) > "
            f"[User banned:{self.banned}, priority:{self.priority}]"
        )
