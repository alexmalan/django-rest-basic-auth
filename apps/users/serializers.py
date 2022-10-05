"""
User serializer.
"""
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """

    class Meta:
        """
        Meta class.
        """

        model = User
        fields = ("username", "password", "role", "deposit")
