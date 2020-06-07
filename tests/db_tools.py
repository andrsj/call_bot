from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from call_bot.models.phones import Phone
from call_bot.settings import SQL_URL


engine = create_engine(SQL_URL, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def get_all_test_phones_str():
    return [
        f'{phone.name} : {phone.phone} '
        f'[p:{phone.priority} b:{phone.banned}]'
        for phone in session.query(Phone)
        .order_by(Phone.name)
        .filter(Phone.name.like('test_user%'))
    ]


def delete_test_users_by_name_like_test_():
    phones = session.query(Phone).filter(Phone.name.like('test_user%'))
    if phones.scalar():
        print('\nExist phones with test_users:\n')
        for phone in phones:
            print(f'Find: {phone}')
            session.delete(phone)
            print(f'\nDelete: {phone}\n')
        session.commit()
        print('\nCommited')
    else:
        print("\nNot found test_phones")
