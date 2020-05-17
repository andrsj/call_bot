from .database import engine, Base
from .phones import Phone
from .session import Session

Session.configure(bind=engine)
