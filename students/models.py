from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# List of all counties in the USA (you might need to load this from your external CSV later)
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

# High school year choices
HIGH_SCHOOL_YEAR_CHOICES = [
    ("pre-highschool", "Pre-Highschool"),
    ("9th", "9th Grade"),
    ("10th", "10th Grade"),
    ("11th", "11th Grade"),
    ("12th", "12th Grade"),
    ("graduate", "Highschool Graduate"),
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
    year_in_highschool = models.CharField(
        max_length=15, choices=HIGH_SCHOOL_YEAR_CHOICES
    )
    county = models.CharField(max_length=10, choices=USA_COUNTIES)
    interests = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["display_name", "year_in_highschool", "county"]

    def __str__(self):
        return self.username
