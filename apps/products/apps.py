"""
Product app configurations.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Product application configuration.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
