from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    profile_description = models.TextField()
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50, choices=[('member', 'Member'), ('caregiver', 'Caregiver')])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Specify the field used for authentication
    REQUIRED_FIELDS = ['given_name', 'surname']

class Caregiver(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "FEMALE", 'Female'
        MALE = "MALE", 'Male'
    class Type(models.TextChoices):
        BABYSITTER = "BABYSITTER", 'Babysitter'
        CAREGIVER_FOR_ELDERLY = "CAREGIVER_FOR_ELDERLY", 'Caregiver for elderly'
        PLAYMATE_FOR_CHILDREN = "PLAYMATE_FOR_CHILDREN", 'Playmate for children'
    caregiver_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='uploads/')
    gender = models.CharField(max_length=50, choices=Gender.choices)
    caregiving_type = models.CharField(max_length=50, choices=Type.choices)
    hourly_rate = models.FloatField()

class Member(models.Model):
    member_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    house_rules = models.TextField()

class Address(models.Model):
    member_user = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    town = models.CharField(max_length=255)

class Job(models.Model):
    class Type(models.TextChoices):
        BABYSITTER = "BABYSITTER", 'Babysitter'
        CAREGIVER_FOR_ELDERLY = "CAREGIVER_FOR_ELDERLY", 'Caregiver for elderly'
        PLAYMATE_FOR_CHILDREN = "PLAYMATE_FOR_CHILDREN", 'Playmate for children'
    job_id = models.AutoField(primary_key=True)
    member_user = models.ForeignKey(Member, on_delete=models.CASCADE)
    required_caregiving_type = models.CharField(max_length=50, choices=Type.choices)
    other_requirements = models.TextField()
    date_posted = models.DateField()

class JobApplication(models.Model):
    caregiver_user = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateField()

class Appointment(models.Model):
    class Choice(models.TextChoices):
        SCHEDULED = "SCHEDULED", 'Scheduled'
        PENDING = "PENDING", 'Pending'
        CANCELLED = "CANCELLED", 'Cancelled'
    appointment_id = models.AutoField(primary_key=True)
    caregiver_user = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    member_user = models.ForeignKey(Member, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    work_hours = models.IntegerField()
    status = models.CharField(max_length=50, choices=Choice.choices)
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new appointment (not updating)
            self.status = Appointment.Choice.PENDING  # Set status to "PENDING" by default

        super().save(*args, **kwargs)

    def change(self, status=None):
        if status == "Scheduled":
            self.status = Appointment.Choice.SCHEDULED
        elif status == "Cancelled":
            self.status = Appointment.Choice.CANCELLED
        else:
            # Handle the case where an invalid status is provided
            raise ValueError("Invalid status provided")

        super().save()

