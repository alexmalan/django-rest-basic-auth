from django.db import models

from apps.users.models import BaseClass, User


class Product(BaseClass):
    name = models.CharField(max_length=255, null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    cost = models.IntegerField(null=False, blank=False, default=0)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
