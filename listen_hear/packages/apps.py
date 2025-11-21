from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PackagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listen_hear.packages'
    verbose_name = _("Packages")
