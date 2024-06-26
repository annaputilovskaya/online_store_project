from django.contrib import admin

from catalog.models import Category, Product, Contacts, ProductVersion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("country", "address", "inn")


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ("version_number", "version_name", "is_active", "product")
    list_filter = ("is_active",)
