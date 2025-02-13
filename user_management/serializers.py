from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Registration

class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Required for registration
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserProfileRegistrationSerializer()  

    class Meta:
        model = Registration
        fields = '__all__' 
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserProfileRegistrationSerializer().create(user_data) 
        registration = Registration.objects.create(user=user, **validated_data)  
        return registration

    def to_representation(self, instance):
        """Override to hide phone number from other users."""
        ret = super().to_representation(instance)
        user = self.context['request'].user
        if user != instance.user:
            ret.pop('phone_number')  # Hide phone number from other users
        return ret
    
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
