"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from core.models import Spin, UserPrize, Prize
from django.utils.translation import gettext as _
from django.db import transaction

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    @transaction.atomic
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user= get_user_model().objects.create_user(**validated_data)
        Spin.objects.create(user=user,remaining_spins=3)
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class SpinSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Spin
        fields = ['user', 'remaining_spins']


class UserPrizeSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = UserPrize
        fields = ['user', 'prize']
        extra_kwargs = {'user': {'read_only': True}}
    
    @transaction.atomic    
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        prize_to_deacrese = Prize.objects.filter(pk=validated_data.get('prize').id).first()
        user_spins = Spin.objects.filter(user=validated_data.get('user').id).first()
        
        if prize_to_deacrese.remaining_quantity <= 0:
            raise Exception("No remaining prizez for prize: ",prize_to_deacrese.name)
        
        if user_spins.remaining_spins <= 0:
            raise Exception("No remaining spins for user: ",user_spins.user.name)
        
        user_spins.update(remaining_spins=(user_spins.remaining_spins-1))
        prize_to_deacrese.update(remaining_quantity=(prize_to_deacrese.remaining_quantity-1))

        userprize= UserPrize.objects.create(**validated_data)
        return userprize