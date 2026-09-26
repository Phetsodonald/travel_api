from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserBaseSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'date_of_birth',
            'bio',
            'profile_picture',
            'travel_preferences',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'full_name',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }


class UserSerializer(UserBaseSerializer):
    pass


class RegistrationSerializer(UserBaseSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='Password with at least 8 characters.'
    )

    password_confirm = serializers.CharField(
        write_only=True,
        help_text='Repeat password.'
    )

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            'password_confirm',
        ]

    def validate(self, data):

        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })

        return data

    def create(self, validated_data):

        validated_data.pop('password_confirm')

        password = validated_data.pop('password')

        return User.objects.create_user(
            password=password,
            **validated_data
        )


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        help_text='Username used for login.'
    )

    password = serializers.CharField(
        write_only=True,
        help_text='Account password.'
    )

    def validate(self, data):

        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError(
                'Invalid credentials.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Account is inactive.'
            )

        data['user'] = user

        return data


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate_old_password(self, value):

        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                'Current password is incorrect.'
            )

        return value