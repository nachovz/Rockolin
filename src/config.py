# -*- coding: utf-8 -*-
"""App configuration."""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    'auth_store_class': 'tipfy.auth.MultiAuthStore',
}

config['tipfy.sessions'] = {
    'secret_key': 'XXXXXXXXXXXXXXX',
}

config['tipfy.auth.facebook'] = {
    'api_key':    '283934171634741',
    'app_secret': '6a16d773ecd9f178e75b0a778ec636d4 ',
}

config['tipfy.auth.friendfeed'] = {
    'consumer_key':    'XXXXXXXXXXXXXXX',
    'consumer_secret': 'XXXXXXXXXXXXXXX',
}

config['tipfy.auth.twitter'] = {
    'consumer_key':    'o6j5ow67Rk6trS5WnRgXPA',
    'consumer_secret': 'hFKfwAZ77MPmEhRMgtKwsoolsQSXyVhTabzSgBn3Eg',
}

config['tipfyext.jinja2'] = {
    'environment_args': {
        'autoescape': True,
        'extensions': [
            'jinja2.ext.autoescape',
            'jinja2.ext.i18n',
            'jinja2.ext.with_'
        ],
    },
}
