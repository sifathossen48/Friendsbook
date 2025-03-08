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
    address = models.CharField(max_length=50)
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Access the sender and receiver's full names from the linked Registration model
        sender_name = self.sender.profile.name  # Assuming the related name for Registration is 'profile'
        receiver_name = self.receiver.profile.name
        return f"{sender_name} -> {receiver_name}: {self.message}"