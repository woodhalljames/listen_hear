from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EstimatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listen_hear.estimates'
    verbose_name = _("Estimates")
