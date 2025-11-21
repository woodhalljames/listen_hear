
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, URLField, ImageField, DateTimeField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Listen Hear.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    # Builder profile fields
    company_name = CharField(_("Company Name"), max_length=255, blank=True)
    contact_person = CharField(_("Contact Person"), max_length=255, blank=True)
    phone = CharField(_("Phone Number"), max_length=20, blank=True)
    bio = TextField(_("Bio"), blank=True)
    website = URLField(_("Website"), blank=True)
    avatar = ImageField(_("Avatar"), upload_to="avatars/", blank=True)
    profile_created_at = DateTimeField(_("Profile Created At"), auto_now_add=True, null=True)
    profile_updated_at = DateTimeField(_("Profile Updated At"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
