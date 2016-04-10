"""
Django settings for drs project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4a1gg4s#qiyti*dxuq+xfq@msqr4p_8(wb!k_xznv+5ph*1$tm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'drs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


def monkey_patch():
    def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Similar to smart_text, except that lazy instances are resolved to
        strings, rather than kept as lazy objects.
        If strings_only is True, don't convert (some) non-string-like objects.
        """
        # Handle the common case first for performance reasons.
        if issubclass(type(s), six.text_type):
            return s
        if strings_only and is_protected_type(s):
            return s
        try:
            if not issubclass(type(s), six.string_types):
                if six.PY3:
                    if isinstance(s, bytes):
                        s = six.text_type(s, encoding, errors)
                    else:
                        s = six.text_type(s)
                elif hasattr(s, '__unicode__'):
                    s = six.text_type(s)
                else:
                    s = six.text_type(bytes(s), encoding, errors)
            else:
                # Note: We use .decode() here, instead of six.text_type(s, encoding,
                # errors), so that if s is a SafeBytes, it ends up being a
                # SafeText at the end.
                s = s.decode(encoding, errors)
        except UnicodeDecodeError as e:
            if not isinstance(s, Exception):
                raise DjangoUnicodeDecodeError(s, *e.args)
            else:
                # If we get to here, the caller has passed in an Exception
                # subclass populated with non-ASCII bytestring data without a
                # working unicode method. Try to handle this without raising a
                # further exception by individually forcing the exception args
                # to unicode.
                s = ' '.join(force_text(arg, encoding, strings_only, errors)
                             for arg in s)
        return s

    import six
    from django.utils.encoding import is_protected_type
    import django.utils.encoding
    django.utils.encoding.force_text = force_text
monkey_patch()
