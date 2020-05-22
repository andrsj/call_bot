from call_bot.models.database import engine, Base
from call_bot.models.phones import Phone
from call_bot.models.session import Session

Session.configure(bind=engine)
session = Session()
