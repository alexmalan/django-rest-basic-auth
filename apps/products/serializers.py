from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "amount", "cost", "user_id")
        write_only_fields = (
            "name",
            "amount",
            "cost",
        )
        read_only_fields = (
            "id",
            "user_id",
        )
