from django.apps import AppConfig


class KiteRunnerConfig(AppConfig):
    name = "kite_runner"
    verbose_name = "KiteRunner"

    def ready(self):
        from . import signals
