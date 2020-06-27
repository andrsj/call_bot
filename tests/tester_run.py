from distest import TestCollector, run_dtest_bot
from distest.TestInterface import TestInterface
from distest.exceptions import ResponseDidNotMatchError
from itertools import count
from copy import copy
import sys


from call_bot.messages import ManagerMessages
from call_bot.models.phones import Phone
from tests.db_tools import (
    delete_test_users_by_name_like_test_,
    get_all_test_phones_str,
    get_all_test_priority_phones_str,
    get_all_test_ban_phones_str
)


test_collector = TestCollector()

test_user_01 = Phone('001', 'test_user_01')
test_user_02_b = Phone('002', 'test_user_02', banned=True)
test_user_03_p = Phone('003', 'test_user_03', priority=True)


@test_collector()
async def test_conf(interface: TestInterface):
    command = 'conf'
    test_cases = (
        (command,          ManagerMessages.get_message_value_of_conf(command, 'off')),
        (command + ' on',  ManagerMessages.get_message_succesfully_update_config(command, 'on')),
        (command,          ManagerMessages.get_message_value_of_conf(command, 'on')),
        (command + ' on',  ManagerMessages.get_message_already_set_config(command, 'on')),
        (command + ' off', ManagerMessages.get_message_succesfully_update_config(command, 'off'))
    )
    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_aa(interface: TestInterface):
    command = 'aa'
    test_cases = (
        (command,             ManagerMessages.get_message_value_of_conf(command, 'off')),
        (command + ' on',     ManagerMessages.get_message_succesfully_update_config(command, 'on')),
        (command,             ManagerMessages.get_message_value_of_conf(command, 'on')),
        (command + ' on',     ManagerMessages.get_message_already_set_config(command, 'on')),
        (command + ' off',    ManagerMessages.get_message_succesfully_update_config(command, 'off')),
        (command + ' blabla', ManagerMessages.get_message_not_int_or_on_off_value('blabla')),
        (command + ' 10',     ManagerMessages.get_message_succesfully_update_config(command, '10'))
    )

    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_autotake(interface: TestInterface):
    command = 'autotake'
    test_cases = (
        (command,             ManagerMessages.get_message_value_of_conf(command, 'off')),
        (command + ' on',     ManagerMessages.get_message_succesfully_update_config(command, 'on')),
        (command,             ManagerMessages.get_message_value_of_conf(command, 'on')),
        (command + ' on',     ManagerMessages.get_message_already_set_config(command, 'on')),
        (command + ' off',    ManagerMessages.get_message_succesfully_update_config(command, 'off')),
        (command + ' blabla', ManagerMessages.get_message_not_int_or_on_off_value('blabla')),
        (command + ' 10',     ManagerMessages.get_message_succesfully_update_config(command, '10'))
    )

    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_set_main(interface: TestInterface):
    command = 'set main'
    test_cases = (
            (
                command,
                ManagerMessages.get_message_miss_required_param('channel: str')
            ),
            (
                command + ' main',
                ManagerMessages.get_message_already_set_channel('main', 'main')
            ),
            (
                command + ' other_main',
                ManagerMessages.get_message_succesfully_update_channel('main', 'other_main')
            )
    )

    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_set_public(interface: TestInterface):
    command = 'set public'
    test_cases = (
        (
            command,
            ManagerMessages.get_message_miss_required_param('channel: str')
        ),
        (
            command + ' public',
            ManagerMessages.get_message_already_set_channel('public', 'public')
        ),
        (
            command + ' other_public',
            ManagerMessages.get_message_succesfully_update_channel('public', 'other_public')
        )
    )

    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_set_sound(interface: TestInterface):
    command = 'set sound'
    test_cases = (
        (
            command,
            ManagerMessages.get_message_miss_required_param('channel: str')
        ),
        (
            command + ' sound',
            ManagerMessages.get_message_already_set_channel('sound', 'sound')
        ),
        (
            command + ' other_sound',
            ManagerMessages.get_message_succesfully_update_channel('sound', 'other_sound')
        )
    )

    await interface.send_message('set default')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_set(interface: TestInterface):
    command = 'set'
    test_cases = (
        (
            command + ' default',
            ManagerMessages.get_message_succesfully_set_default()
        ),
    )

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_save(interface: TestInterface):
    command = 'save'

    test_cases = (
        (
            f'{command} {test_user_01.phone} {test_user_01.name}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_01)
        ),
        (
            f'{command} {test_user_01.phone} fake',
            ManagerMessages.get_message_phone_already_exist('number', test_user_01.phone)
        ),
        (
            f'{command} 004 {test_user_01.name}',
            ManagerMessages.get_message_phone_already_exist('name', test_user_01.name)
        ),
        (
            f'{command} {test_user_02_b.phone} {test_user_02_b.name} {test_user_02_b.priority} {test_user_02_b.banned}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_02_b)
        ),
        (
            f'{command} {test_user_03_p.phone} {test_user_03_p.name} {test_user_03_p.priority} {test_user_03_p.banned}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_03_p)
        )
    )

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_edit(interface: TestInterface):
    command = 'edit'

    test_user_01_updated = copy(test_user_01)
    test_user_01_updated.name = 'test_user_01x'
    test_user_01_updated.phone = '011'

    test_cases = (
        (
            f'{command} name {test_user_01.phone} {test_user_01_updated.name}',
            ManagerMessages.get_message_succesfully_update_phone(
                test_user_01.phone,
                'Name',
                test_user_01_updated.name
            )
        ),
        (
            f'{command} number {test_user_01.phone} {test_user_01_updated.phone}',
            ManagerMessages.get_message_succesfully_update_phone(
                test_user_01.phone,
                'Phone',
                test_user_01_updated.phone
            )
        ),
        (
            f'{command}',
            ManagerMessages.get_message_help_edit()
        ),
        (
            f'{command} name 0000 0001',
            ManagerMessages.get_message_not_found_phone('0000')
        )
    )

    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',
    )

    await test_with_fixtures(interface, fixtures, test_cases)


@test_collector()
async def test_pb(interface: TestInterface):
    command = 'pb'

    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',

        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    await wait_embed_message(interface, fixtures, command, get_all_test_phones_str)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_priorlist(interface: TestInterface):
    command = 'priorlist'

    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',

        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    await wait_embed_message(interface, fixtures, command, get_all_test_priority_phones_str)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_banlist(interface: TestInterface):
    command = 'banlist'

    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',

        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    await wait_embed_message(interface, fixtures, command, get_all_test_ban_phones_str)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_prior(interface: TestInterface):
    command = 'prior'

    test_user_01_updated = copy(test_user_01)
    test_user_01_updated.priority = True

    test_user_04 = Phone('004', 'test_user_04')
    test_user_04_updated = copy(test_user_04)
    test_user_04_updated.priority = True

    test_user_05 = Phone('005', 'test_user_05')
    test_user_05_updated = copy(test_user_05)
    test_user_05_updated.priority = True

    test_cases = (
        (
            f'{command} {test_user_01.phone} {test_user_01.name}',
            ManagerMessages.get_message_succesfully_update_phone_prioritet(test_user_01_updated)),
        (
            f'{command} {test_user_03_p.phone} {test_user_03_p.name}',
            ManagerMessages.get_message_phone_already_in('priority')
        ),
        (
            f'{command} {test_user_04.phone}',
            ManagerMessages.get_message_succesfully_update_phone_prioritet(test_user_04_updated)
        ),
        (
            f'{command} {test_user_05.phone} {test_user_05.name}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_05_updated)
        ),
        (
            f'{command} 0000',
            ManagerMessages.get_message_not_found_number()
        ),
        (
            f'{command} 001 blablabla',
            ManagerMessages.get_message_phone_already_exist_()
        ),
        (
            f'{command} 0000 {test_user_01.name}',
            ManagerMessages.get_message_phone_already_exist_()
        )
    )

    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',

        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}',

        f'save {test_user_04.phone} {test_user_04.name}'
    )

    await test_with_fixtures(interface, fixtures, test_cases)


@test_collector()
async def test_priordel(interface: TestInterface):
    command = 'priordel'
    fixtures = (
        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    test_cases = (
        (
            f'{command} {test_user_03_p.phone}',
            ManagerMessages.get_message_succesfully_remove_prior_number(test_user_03_p.phone)
        ),
        (
            f'{command} {test_user_02_b.phone}',
            ManagerMessages.get_message_phone_already_in('not priority')
        ),
        (
            f'{command} 0001',
            ManagerMessages.get_message_not_found_phone('0001')
        )
    )

    await test_with_fixtures(interface, fixtures, test_cases)


@test_collector()
async def test_unban(interface: TestInterface):
    command = 'unban'
    fixtures = (
        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    test_cases = (
        (
            f'{command} {test_user_02_b.phone}',
            ManagerMessages.get_message_succesfully_remove_ban_number(test_user_02_b.phone)
        ),
        (
            f'{command} {test_user_03_p.phone}',
            ManagerMessages.get_message_phone_already_in('unban')
        ),
        (
            f'{command} 0001',
            ManagerMessages.get_message_not_found_phone('0001')
        )
    )

    await test_with_fixtures(interface, fixtures, test_cases)


@test_collector()
async def test_ban(interface: TestInterface):
    command = 'ban'
    fixtures = (
        f'save {test_user_02_b.phone} {test_user_02_b.name} '
        f'{test_user_02_b.priority} {test_user_02_b.banned}',

        f'save {test_user_03_p.phone} {test_user_03_p.name} '
        f'{test_user_03_p.priority} {test_user_03_p.banned}'
    )

    test_cases = (
        (
            f'{command} {test_user_02_b.phone}',
            ManagerMessages.get_message_phone_already_in('ban')
        ),
        (
            f'{command} {test_user_03_p.phone}',
            ManagerMessages.get_message_succesfully_ban_number(test_user_03_p.phone)
        ),
        (
            f'{command} 0001',
            ManagerMessages.get_message_not_found_phone('0001')
        )
    )

    await test_with_fixtures(interface, fixtures, test_cases)


@test_collector()
async def test_deletephone(interface: TestInterface):
    command = 'deletephone'
    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name} '
        f'{test_user_01.priority} {test_user_01.banned}',
    )

    test_cases = (
        (
            f'{command} {test_user_01.phone}',
            ManagerMessages.get_message_succesfully_delete_phone(test_user_01.phone)
        ),
        (
            f'{command} 0001',
            ManagerMessages.get_message_not_found_phone('0001')
        )
    )

    await test_with_fixtures(interface, fixtures, test_cases)


async def test_with_fixtures(interface: TestInterface, fixtures, test_cases):
    for fixture in fixtures:
        await interface.send_message(fixture)
        await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)

    delete_test_users_by_name_like_test_()


async def wait_embed_message(interface: TestInterface, fixtures, command, getter):
    for fixture in fixtures:
        await interface.send_message(fixture)
        await interface.wait_for_message()

    await interface.send_message(command)
    message = await interface.wait_for_message()

    counter = count(1)
    count_of_message = 0

    while len(message.embeds) == 0 and count_of_message < len(fixtures):
        count_of_message = next(counter)
        message = await interface.wait_for_message()

    if len(message.embeds) != 1:
        raise ResponseDidNotMatchError('Message have no one or more than one embeds')
    if len(message.embeds[0].fields) != 1:
        raise ResponseDidNotMatchError('Embed have no one or more than one fields')

    for phone in getter():
        if phone not in message.embeds[0].fields[0].value:
            print(phone)
            print(message.embeds[0].fields[0].value)
            print('\n'*3)
            raise ResponseDidNotMatchError('Excessive phone in phone book')


if __name__ == "__main__":
    try:
        run_dtest_bot(sys.argv, test_collector)
    finally:
        delete_test_users_by_name_like_test_()
