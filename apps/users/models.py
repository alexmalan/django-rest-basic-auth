from lib2to3.pytree import Base
from tabnanny import verbose

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self, username, password=None, role=None, deposit=None, **extra_fields
    ):
        if username is None:
            raise TypeError("Users should have a username")

        email = self.normalize_email(username)
        user = self.model(username=email, role=role, deposit=deposit, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, password=None, role=None, deposit=None, **extra_fields
    ):
        if password is None:
            raise TypeError("Password should not be none")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, role, deposit, **extra_fields)


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RoleChoices(models.TextChoices):
    SELLER = "SELLER"
    BUYER = "BUYER"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=250, null=False, blank=False)
    deposit = models.IntegerField(
        default=0,
        null=False,
    )
    role = models.CharField(
        max_length=255,
        default=RoleChoices.BUYER,
        choices=RoleChoices.choices,
        null=False,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role", "deposit"]

    objects = UserManager()

    def __repr__(self):
        return f"{self.username}: {self.role}"

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
