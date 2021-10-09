"""This class contain add config."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """This is poll config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
