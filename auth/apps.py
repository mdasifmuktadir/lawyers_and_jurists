from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth'
    label = 'user_auth1232'  # avoids clashing with django.contrib.auth's app label
