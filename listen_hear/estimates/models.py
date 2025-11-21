from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from listen_hear.packages.models import PackageTemplate


class Estimate(models.Model):
    """Generated estimates for builders"""
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("contacted", _("Contacted")),
        ("converted", _("Converted")),
        ("archived", _("Archived")),
    ]

    estimate_number = models.CharField(
        _("Estimate Number"),
        max_length=50,
        unique=True,
        help_text=_("Auto-generated (e.g., EST-2024-001)")
    )
    builder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="estimates",
        verbose_name=_("Builder")
    )
    client_name = models.CharField(_("Client Name"), max_length=255, blank=True, help_text=_("Homeowner name"))
    client_email = models.EmailField(_("Client Email"), blank=True)
    packages = models.ManyToManyField(
        PackageTemplate,
        through="EstimateItem",
        related_name="estimates",
        verbose_name=_("Packages")
    )
    total_low = models.DecimalField(_("Total Low"), max_digits=12, decimal_places=2, help_text=_("Sum of price_low"))
    total_high = models.DecimalField(_("Total High"), max_digits=12, decimal_places=2, help_text=_("Sum of price_high"))
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        verbose_name = _("Estimate")
        verbose_name_plural = _("Estimates")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.estimate_number} - {self.builder.email}"

    def get_absolute_url(self):
        """Get URL for estimate detail view"""
        return reverse("estimates:detail", kwargs={"estimate_number": self.estimate_number})

    def save(self, *args, **kwargs):
        """Generate estimate number if not set"""
        if not self.estimate_number:
            # Get the current year
            from django.utils import timezone
            year = timezone.now().year
            # Get the last estimate number for this year
            last_estimate = Estimate.objects.filter(
                estimate_number__startswith=f"EST-{year}-"
            ).order_by("-estimate_number").first()

            if last_estimate:
                # Extract the number and increment
                last_num = int(last_estimate.estimate_number.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.estimate_number = f"EST-{year}-{new_num:03d}"

        super().save(*args, **kwargs)


class EstimateItem(models.Model):
    """Through table for Estimate and PackageTemplate with snapshot data"""
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Estimate")
    )
    package = models.ForeignKey(
        PackageTemplate,
        on_delete=models.CASCADE,
        verbose_name=_("Package")
    )
    price_low_snapshot = models.DecimalField(
        _("Price Low Snapshot"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Snapshot at time of estimate")
    )
    price_high_snapshot = models.DecimalField(
        _("Price High Snapshot"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Snapshot at time of estimate")
    )
    package_name_snapshot = models.CharField(
        _("Package Name Snapshot"),
        max_length=255,
        help_text=_("In case package is deleted/renamed")
    )

    class Meta:
        verbose_name = _("Estimate Item")
        verbose_name_plural = _("Estimate Items")
        unique_together = ["estimate", "package"]

    def __str__(self):
        return f"{self.estimate.estimate_number} - {self.package_name_snapshot}"
