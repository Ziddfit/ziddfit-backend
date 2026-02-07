from django.apps import AppConfig


class PlanConfig(AppConfig):
    name = 'Plan'
    def ready(self):
        import Plan.signals
