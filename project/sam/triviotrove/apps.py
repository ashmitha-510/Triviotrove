from django.apps import AppConfig

class TriviotroveConfig(AppConfig):  # ✅ Class name should follow PascalCase
    name = "triviotrove"  # ✅ Ensure this matches your app name
    default_auto_field = "django.db.models.BigAutoField"  # ✅ Recommended for Django 3.2+

    def ready(self):
        import triviotrove.signals  # ✅ Ensure signals are imported correctly
