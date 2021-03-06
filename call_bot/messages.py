from call_bot.models.phones import Phone


class ManagerMessages:
    @staticmethod
    def get_message_succesfully_update_channel(group, channel):
        return f'\'{group}\' succesfully update to \'{channel}\''

    @staticmethod
    def get_message_already_set_channel(group, channel):
        return f'\'{group}\' is already set \'{channel}\''

    @staticmethod
    def get_message_succesfully_set_default():
        return 'Bot configuration succesfully set to default values'

    @staticmethod
    def get_message_miss_required_param(param):
        return f'U miss required parametr \'{param}\''

    @staticmethod
    def get_message_not_found_set_group(value):
        return f'Not found group: \'{value}\''

    @staticmethod
    def get_message_succesfully_update_config(name, value):
        return f'Config \'{name}\' succsesfully updated to \'{value}\''

    @staticmethod
    def get_message_already_set_config(name, value):
        return f'Config \'{name}\' already set to \'{value}\''

    @staticmethod
    def get_message_not_int_or_on_off_value(value):
        return f'\'{value}\' -> it is not int or \'on\\off\' value'

    @staticmethod
    def get_message_value_of_conf(conf, value):
        return f'{conf} : {value}'

    @staticmethod
    def get_message_phone_already_exist(property_name, property_value):
        return f'User with this {property_name} \'{property_value}\' ' \
               'is already exist\n' \
               'U can use \'pb\' command for searching in phone book'

    @staticmethod
    def get_message_succesfully_add_phone(phone_model: Phone):
        return f'Add done: {phone_model}'

    @staticmethod
    def get_message_succesfully_update_phone(phone, value, new):
        return f'{value} in \'{phone}\' succesfully updated on \'{new}\''

    @staticmethod
    def get_message_succesfully_delete_phone(phone):
        return f'Phone \'{phone}\' succesfully delete'

    @staticmethod
    def get_message_not_found_phone(phone):
        return f'User by \'{phone}\' not found!'

    @staticmethod
    def get_message_phone_already_in(value):
        return f'This number already in {value}'

    @staticmethod
    def get_message_succesfully_remove_prior_number(number):
        return f'Priority succesfully remove from phone {number}'

    @staticmethod
    def get_message_succesfully_ban_number(number):
        return f'Ban succesfully set for phone {number}'

    @staticmethod
    def get_message_succesfully_remove_ban_number(number):
        return f'Ban succesfully remove from phone {number}'

    @staticmethod
    def get_message_succesfully_update_phone_prioritet(phone):
        return f"'{phone.phone}' succesfully updated priority to 'True'"

    @staticmethod
    def get_message_not_found_number():
        return 'This phone number not found in phone book\n' \
               'Check in \'pb\' for searching'

    @staticmethod
    def get_message_phone_already_exist_():
        return 'This user already exist in phone book\n' \
               'Check in \'pb\' for searching'

    @staticmethod
    def get_message_help_edit():
        return 'Look on `help edit` for more info'

    @staticmethod
    def phone_format(phone, name, prior, ban):
        return f'{name} : {phone} ' \
               f'[p:{prior} b:{ban}]'
