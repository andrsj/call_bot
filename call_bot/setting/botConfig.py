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

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def get_value_channel(self, group: str):
        if group == 'main':
            return self.main
        elif group == 'public':
            return self.public
        elif group == 'sound':
            return self.sound
        else:
            raise ValueError(f'Not found group, check in {self.list_of_channels}')

    def set_value_channel(self, group: str, value):
        if group == 'main':
            self.main = value
        elif group == 'public':
            self.public = value
        elif group == 'sound':
            self.sound = value
        else:
            raise ValueError('Not found group')
        config['channels'][group] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    def get_config_boolean_value(self, name):
        if name == 'autotake':
            return self.autotake
        elif name == 'aa':
            return self.aa
        elif name == 'conf':
            return self.conf
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_boolean}')

    def set_config_boolean_value(self, name: str, value: bool):
        if name == 'autotake':
            self.autotake = value
        elif name == 'aa':
            self.aa = value
        elif name == 'conf':
            self.conf = value
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_boolean}')
        config['conf'][name]['value'] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    def get_config_int_value(self, name: str):
        if name == 'autotake':
            return self.autotake_sec
        elif name == 'aa':
            return self.aa_sec
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_int}')

    def set_config_int_value(self, name: str, value: int):
        if name == 'autotake':
            self.autotake_sec = value
        elif name == 'aa':
            self.aa_sec = value
        else:
            raise ValueError(f'Not found config parametr, check in {Config.list_of_configs_int}')
        config['conf'][name]['sec'] = value
        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    def set_default(self):
        with open('default_bot_configuration.yaml') as conf_def_file:
            config_default = yaml.full_load(conf_def_file)

        for channel in self.list_of_channels:
            self.set_value_channel(channel, config_default['channels'][channel])

        for conf in self.list_of_configs_boolean:
            self.set_config_boolean_value(conf, config_default['conf'][conf]['value'])

        for conf in self.list_of_configs_int:
            self.set_config_int_value(conf, config_default['conf'][conf]['sec'])

    def set_logging_channel(self, name: str, id_channel: int):
        self.logging['name'] = name
        self.logging['id'] = id_channel

        config['channels']['logs']['name'] = name
        config['channels']['logs']['id'] = id_channel

        with open('bot_configuration.yaml', 'w') as configfilewrite:
            yaml.dump(config, configfilewrite)

    def get_logging_channel_name(self):
        return self.logging['name']

    def get_logging_channel_id(self):
        return self.logging['id']


config_bot = Config()
