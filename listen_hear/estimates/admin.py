from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Estimate, EstimateItem


class EstimateItemInline(admin.TabularInline):
    model = EstimateItem
    extra = 0
    readonly_fields = ["package_name_snapshot", "price_low_snapshot", "price_high_snapshot"]
    fields = ["package", "package_name_snapshot", "price_low_snapshot", "price_high_snapshot"]


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = [
        "estimate_number",
        "builder",
        "client_name",
        "total_low",
        "total_high",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["estimate_number", "builder__email", "builder__company_name", "client_name", "client_email"]
    readonly_fields = ["estimate_number", "created_at", "updated_at"]
    inlines = [EstimateItemInline]
    fieldsets = (
        (None, {
            "fields": ("estimate_number", "builder", "status")
        }),
        (_("Client Information"), {
            "fields": ("client_name", "client_email")
        }),
        (_("Totals"), {
            "fields": ("total_low", "total_high", "notes")
        }),
        (_("Timestamps"), {
            "fields": ("created_at", "updated_at")
        }),
    )
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    def get_readonly_fields(self, request, obj=None):
        """Make more fields readonly after creation"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ["builder"]
        return self.readonly_fields


@admin.register(EstimateItem)
class EstimateItemAdmin(admin.ModelAdmin):
    list_display = [
        "estimate",
        "package",
        "package_name_snapshot",
        "price_low_snapshot",
        "price_high_snapshot",
    ]
    list_filter = ["estimate__status"]
    search_fields = ["estimate__estimate_number", "package__name", "package_name_snapshot"]
    readonly_fields = []
