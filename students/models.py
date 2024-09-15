from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import FileExtensionValidator

# List of all counties in the USA with states
USA_COUNTIES = [
    ("AL", "US001", "Autauga County"),
    ("AL", "US003", "Baldwin County"),
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


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    year_in_highschool = models.CharField(
        max_length=15, choices=HIGH_SCHOOL_YEAR_CHOICES
    )
    county = models.CharField(
        max_length=10,
        choices=[
            (f"{state} - {county_code}", f"{state} - {county_name}")
            for state, county_code, county_name in USA_COUNTIES
        ],
    )
    interests = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    num_connections = models.IntegerField(default=0)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    connected = models.BooleanField(default=False)
    activity = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    connected_users = models.ManyToManyField(
        "self", symmetrical=False, related_name="connections", blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["display_name", "year_in_highschool", "county"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Opportunity(models.Model):
    INTERNSHIP = "internship"
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    TYPE_CHOICES = [
        (INTERNSHIP, "Internship"),
        (FULL_TIME, "Full-time"),
        (PART_TIME, "Part-time"),
    ]

    ENTRY_LEVEL = "entry-level"
    ONE_TWO_YEARS = "1-2-years"
    THREE_FIVE_YEARS = "3-5-years"
    FIVE_PLUS_YEARS = "5-plus-years"
    EXPERIENCE_CHOICES = [
        (ENTRY_LEVEL, "Entry Level"),
        (ONE_TWO_YEARS, "1-2 years"),
        (THREE_FIVE_YEARS, "3-5 years"),
        (FIVE_PLUS_YEARS, "5+ years"),
    ]

    SAN_FRANCISCO = "san-francisco"
    NEW_YORK = "new-york"
    AUSTIN = "austin"
    CHICAGO = "chicago"
    REMOTE = "remote"
    LOCATION_CHOICES = [
        (SAN_FRANCISCO, "San Francisco, CA"),
        (NEW_YORK, "New York, NY"),
        (AUSTIN, "Austin, TX"),
        (CHICAGO, "Chicago, IL"),
        (REMOTE, "Remote"),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255)  # Comma-separated tags
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    saved_by = models.ManyToManyField(
        User, related_name="saved_opportunities", blank=True
    )
    applied_by = models.ManyToManyField(
        User, related_name="applied_opportunities", blank=True
    )

    def __str__(self):
        return self.title
