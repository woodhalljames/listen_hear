from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    """Top-level grouping for packages (e.g., Audio, Security, Lighting)"""
    name = models.CharField(_("Category Name"), max_length=255)
    image = models.ImageField(_("Category Image"), upload_to="categories/", blank=True)
    description = models.TextField(_("Description"), blank=True)
    order = models.IntegerField(_("Display Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """Nested category under Category (e.g., Whole Home Audio, Outdoor Audio)"""
    name = models.CharField(_("SubCategory Name"), max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name=_("Category")
    )
    image = models.ImageField(_("SubCategory Image"), upload_to="subcategories/", blank=True)
    description = models.TextField(_("Description"), blank=True)
    order = models.IntegerField(_("Display Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("SubCategory")
        verbose_name_plural = _("SubCategories")
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class InstallPhase(models.Model):
    """Installation phases (e.g., Pre-Wire, Rough-In, Finish)"""
    name = models.CharField(_("Phase Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    order = models.IntegerField(_("Display Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Install Phase")
        verbose_name_plural = _("Install Phases")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class PackageTemplate(models.Model):
    """The actual products/packages (tiered: Good/Better/Best)"""
    name = models.CharField(_("Package Name"), max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="packages",
        verbose_name=_("Category")
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
        verbose_name=_("SubCategory"),
        help_text=_("Not mandatory for package build")
    )
    image = models.ImageField(_("Package Image"), upload_to="packages/", blank=True)
    description = models.TextField(_("Description"), help_text=_("What's included"))
    price_low = models.DecimalField(_("Price Low"), max_digits=10, decimal_places=2, help_text=_("Estimated price range - low"))
    price_high = models.DecimalField(_("Price High"), max_digits=10, decimal_places=2, help_text=_("Estimated price range - high"))
    price_notes = models.TextField(_("Price Notes"), blank=True, help_text=_("Disclaimers/asterisks"))
    install_phases = models.ManyToManyField(
        InstallPhase,
        blank=True,
        related_name="packages",
        verbose_name=_("Install Phases")
    )
    requires_phase = models.ForeignKey(
        InstallPhase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="required_by_packages",
        verbose_name=_("Required Phase"),
        help_text=_("Installation phase this package requires")
    )
    bundle_discount_note = models.CharField(
        _("Bundle Discount Note"),
        max_length=255,
        blank=True,
        help_text=_("e.g., Save $X when combined with Y")
    )
    utility_incentive_eligible = models.BooleanField(
        _("Utility Incentive Eligible"),
        default=False,
        help_text=_("Eligible for utility incentives")
    )
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Package Template")
        verbose_name_plural = _("Package Templates")
        ordering = ["category", "subcategory", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get URL for package detail view"""
        return reverse("packages:detail", kwargs={"pk": self.pk})
