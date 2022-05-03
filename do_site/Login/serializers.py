from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user was not found.'
            )
        return {
            'id': user.pk,
            'username': user.username,
            'token': user.token
        }
