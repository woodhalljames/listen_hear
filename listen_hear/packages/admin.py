from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, SubCategory, InstallPhase, PackageTemplate


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {}
    ordering = ["order", "name"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "order", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    ordering = ["category", "order", "name"]


@admin.register(InstallPhase)
class InstallPhaseAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    ordering = ["order", "name"]


@admin.register(PackageTemplate)
class PackageTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "subcategory",
        "price_low",
        "price_high",
        "utility_incentive_eligible",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "category",
        "subcategory",
        "is_active",
        "utility_incentive_eligible",
        "install_phases",
    ]
    search_fields = ["name", "description", "price_notes"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["install_phases"]
    fieldsets = (
        (None, {
            "fields": ("name", "category", "subcategory", "image", "description")
        }),
        (_("Pricing"), {
            "fields": ("price_low", "price_high", "price_notes", "bundle_discount_note", "utility_incentive_eligible")
        }),
        (_("Installation"), {
            "fields": ("install_phases", "requires_phase")
        }),
        (_("Status"), {
            "fields": ("is_active", "created_at", "updated_at")
        }),
    )
    ordering = ["category", "subcategory", "name"]
