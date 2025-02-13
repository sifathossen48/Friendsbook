from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Registration(models.Model):
    PROFILE_CREATED_BY_CHOICES = [
        ('self', 'Self'),
        ('parent', 'Parent'),
        ('siblings', 'Siblings'),
        ('relative', 'Relative'),
        ('friend', 'Friend'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_created_by = models.CharField(max_length=10, choices=PROFILE_CREATED_BY_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    height = models.FloatField()
    preferred_height = models.FloatField(null=True, blank=True)
    age = models.IntegerField()
    preferred_age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField()
    preferred_weight = models.FloatField(null=True, blank=True)
    education = models.CharField(max_length=255)
    preferred_education = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    address = models.TextField()
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)

    def __str__(self):
        return self.name
