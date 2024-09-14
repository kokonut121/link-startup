from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# List of all counties in the USA
USA_COUNTIES = [
    ("US001", "Autauga County"),
    ("US003", "Baldwin County"),
    # Add more counties here...
]

# List of predefined interests
INTEREST_CHOICES = [
    ("sports", "Sports"),
    ("music", "Music"),
    ("technology", "Technology"),
    ("reading", "Reading"),
    ("traveling", "Traveling"),
    # Add more interests here...
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, display_name, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, display_name=display_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, display_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, display_name, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    birthday = models.DateField()
    county = models.CharField(max_length=10, choices=USA_COUNTIES)
    interests = models.CharField(max_length=20, choices=INTEREST_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["display_name", "birthday", "county"]

    def __str__(self):
        return self.username
