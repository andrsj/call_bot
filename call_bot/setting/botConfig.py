import yaml

with open('bot_configuration.yaml') as configfile:
    config = yaml.full_load(configfile)


class Config:
    list_of_channels = ['main', 'public', 'sound']
    list_of_configs_boolean = ['autotake', 'aa', 'conf']
    list_of_configs_int = ['autotake', 'aa']

    main = config['channels']['main']
    public = config['channels']['public']
    sound = config['channels']['sound']

    logging = {
        'name': config['channels']['logs']['name'],
        'id': config['channels']['logs']['id']
    }

    autotake = config['conf']['autotake']['value']
    autotake_sec = config['conf']['autotake']['sec']
    conf = config['conf']['conf']['value']
    aa = config['conf']['aa']['value']
    aa_sec = config['conf']['aa']['sec']

    @classmethod
    def get_value_channel(cls, group):
        if group == 'main':
            return cls.main
        elif group == 'public':
            return cls.public
        elif group == 'sound':
            return cls.sound
        else:
            raise ValueError(f'Not found group, check in {cls.list_of_channels}')

    @classmethod
    def set_value_channel(cls, group, value):
        if group == 'main':
            cls.main = value
        elif group == 'public':
            cls.public = value
        elif group == 'sound':
            cls.sound = value
        else:
            raise ValueError('Not found group')
        config['channels'][group] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    @classmethod
    def get_config_boolean_value(cls, name):
        if name == 'autotake':
            return cls.autotake
        elif name == 'aa':
            return cls.aa
        elif name == 'conf':
            return cls.conf
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_boolean}')

    @classmethod
    def set_config_boolean_value(cls, name, value):
        if name == 'autotake':
            cls.autotake = value
        elif name == 'aa':
            cls.aa = value
        elif name == 'conf':
            cls.conf = value
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_boolean}')
        config['conf'][name]['value'] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    @classmethod
    def get_config_int_value(cls, name):
        if name == 'autotake':
            return cls.autotake_sec
        elif name == 'aa':
            return cls.aa_sec
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_int}')

    @classmethod
    def set_config_int_value(cls, name, value):
        if name == 'autotake':
            cls.autotake_sec = value
        elif name == 'aa':
            cls.aa_sec = value
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_int}')
        config['conf'][name]['sec'] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    @staticmethod
    def set_default():
        with open('default_bot_configuration.yaml') as conf_def_file:
            config_default = yaml.full_load(conf_def_file)

        for channel in Config.list_of_channels:
            Config.set_value_channel(channel, config_default['channels'][channel])

        for conf in Config.list_of_configs_boolean:
            Config.set_config_boolean_value(conf, config_default['conf'][conf]['value'])

        for conf in Config.list_of_configs_int:
            Config.set_config_int_value(conf, config_default['conf'][conf]['sec'])

    @classmethod
    def set_logging_channel(cls, name: str, id_channel: int):
        cls.logging['name'] = name
        cls.logging['id'] = id_channel

        config['channels']['logs']['name'] = name
        config['channels']['logs']['id'] = id_channel

        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    @classmethod
    def get_logging_channel_name(cls):
        return cls.logging['name']

    @classmethod
    def get_logging_channel_id(cls):
        return cls.logging['id']