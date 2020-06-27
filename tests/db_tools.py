from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from call_bot.models.phones import Phone
from call_bot.settings import SQL_URL
from call_bot.messages import ManagerMessages


engine = create_engine(SQL_URL)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def get_all_test_phones_str():
    return [
        ManagerMessages.phone_format(
            phone.phone,
            phone.name,
            phone.priority,
            phone.banned
        )
        for phone in session.query(Phone)
        .order_by(Phone.name)
        .filter(Phone.name.like('test_user%'))
    ]


def get_all_test_priority_phones_str():
    return [
        ManagerMessages.phone_format(
            phone.phone,
            phone.name,
            phone.priority,
            phone.banned
        )
        for phone in session.query(Phone)
        .order_by(Phone.name)
        .filter(Phone.name.like('test_user%'), Phone.priority)
    ]


def get_all_test_ban_phones_str():
    return [
        ManagerMessages.phone_format(
            phone.phone,
            phone.name,
            phone.priority,
            phone.banned
        )
        for phone in session.query(Phone)
        .order_by(Phone.name)
        .filter(Phone.name.like('test_user%'), Phone.banned)
    ]


def delete_test_users_by_name_like_test_():
    phones = session.query(Phone).filter(Phone.name.like('test_user%')).all()
    if phones:
        for phone in phones:
            session.delete(phone)
        session.commit()
