from distest import TestCollector, run_dtest_bot
from distest.TestInterface import TestInterface
from distest.exceptions import ResponseDidNotMatchError
from itertools import count
from copy import copy
import sys


from call_bot.messages import ManagerMessages
from call_bot.models.phones import Phone
from tests.db_tools import delete_test_users_by_name_like_test_, get_all_test_phones_str


test_collector = TestCollector()

test_user_01 = Phone('001', 'test_user_01')
test_user_02 = Phone('002', 'test_user_02', banned=True)
test_user_03 = Phone('003', 'test_user_03', priority=True)


@test_collector()
async def test_conf_command(interface: TestInterface):
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
        await interface.assert_reply_contains(*test_case)


@test_collector()
async def test_aa_command(interface: TestInterface):
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
async def test_autotake_command(interface: TestInterface):
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
async def test_set_main_command(interface: TestInterface):
    command = 'set main'
    test_cases = (
            (
                command,
                ManagerMessages.get_message_miss_required_param_for_channels()
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
async def test_set_public_command(interface: TestInterface):
    command = 'set public'
    test_cases = (
        (
            command,
            ManagerMessages.get_message_miss_required_param_for_channels()
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
async def test_set_sound_command(interface: TestInterface):
    command = 'set sound'
    test_cases = (
        (
            command,
            ManagerMessages.get_message_miss_required_param_for_channels()
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
async def test_set_command(interface: TestInterface):
    command = 'set'
    test_cases = (
        (
            command + ' default',
            ManagerMessages.get_message_succesfully_set_default()
        ),
        (
            command + ' blabla',
            ManagerMessages.get_message_not_found_set_group('blabla')
        ),
    )

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)


@test_collector()
async def test_save_command(interface: TestInterface):
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
            f'{command} {test_user_02.phone} {test_user_02.name} {test_user_02.priority} {test_user_02.banned}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_02)
        ),
        (
            f'{command} {test_user_03.phone} {test_user_03.name} {test_user_03.priority} {test_user_03.banned}',
            ManagerMessages.get_message_succesfully_add_phone(test_user_03)
        )
    )

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_edit_command(interface: TestInterface):
    command = 'edit'

    test_user_01_updated = copy(test_user_01)
    test_user_01_updated.name = 'test_user_01x'

    test_cases = (
        (
            f'{command} {test_user_01.phone} {test_user_01_updated.name}',
            ManagerMessages.get_message_succesfully_update_phone(test_user_01_updated)
        ),
        (
            f'{command} 004 blablabla',
            ManagerMessages.get_message_not_found_phone('004')
        )
    )

    await interface.send_message(f'save {test_user_01.phone} {test_user_01.name}')
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_pb_command(interface: TestInterface):
    fixtures = (
        f'save {test_user_01.phone} {test_user_01.name}',

        f'save {test_user_02.phone} {test_user_02.name} '
        f'{test_user_02.priority} {test_user_02.banned}',

        f'save {test_user_03.phone} {test_user_03.name} '
        f'{test_user_03.priority} {test_user_03.banned}'
    )

    for fixture in fixtures:
        await interface.send_message(fixture)
    await interface.wait_for_message()

    await interface.send_message('pb')
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
    for phone in get_all_test_phones_str():
        if phone not in message.embeds[0].fields[0].value:
            raise ResponseDidNotMatchError('Excessive phone in phone book')

    delete_test_users_by_name_like_test_()


@test_collector()
async def test_prior_command(interface: TestInterface):
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
            f'{command} {test_user_03.phone} {test_user_03.name}',
            ManagerMessages.get_message_phone_already_in_prioritet()
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

        f'save {test_user_02.phone} {test_user_02.name} '
        f'{test_user_02.priority} {test_user_02.banned}',

        f'save {test_user_03.phone} {test_user_03.name} '
        f'{test_user_03.priority} {test_user_03.banned}',

        f'save {test_user_04.phone} {test_user_04.name}'
    )

    for fixture in fixtures:
        await interface.send_message(fixture)
    await interface.wait_for_message()

    for test_case in test_cases:
        await interface.assert_reply_equals(*test_case)

    delete_test_users_by_name_like_test_()


if __name__ == "__main__":
    try:
        run_dtest_bot(sys.argv, test_collector)
    finally:
        delete_test_users_by_name_like_test_()
