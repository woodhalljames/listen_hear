from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listen_hear.cart'
    verbose_name = _("Shopping Cart")
