# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '~/.my.cnf',
            'sql_mode': 'traditional',
        },
    }
}

DEBUG = False