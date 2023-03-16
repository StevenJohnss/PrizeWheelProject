"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from core.models import Spin, UserPrize, Prize, ResetUserPassword
from django.utils.translation import gettext as _
from django.db import transaction
from datetime import datetime, timedelta
import requests
import json


from rest_framework import serializers
from rest_framework.exceptions import APIException

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
    user=UserSerializer(read_only=True)
    #james token 25b2a49f9bb20071824c01b5219763740fbe32f5
    class Meta:
        model = Spin
        fields = ['user', 'remaining_spins']
        extra_kwargs = {'remaining_spins': {'read_only': True}}
    
    def update(self, instance, validated_data):
        """Update and return user."""
        validated_data.pop('remaining_spins', None)
        if(instance.remaining_spins==0):
            raise APIException(f"No remaining spins for user: {instance.user.name}")
        
        validated_data['remaining_spins'] = instance.remaining_spins - 1
        spin = super().update(instance, validated_data)
        spin.save()
        
        return spin


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
        old_user_prizez =  UserPrize.objects.filter(user=validated_data.get('user').id)
        
        if old_user_prizez.length <= 3:
            raise APIException( f"Alredy has {old_user_prizez.length} prizes, thus we cannot add any more prizes for user: {user_spins.user.name}")
        
        if prize_to_deacrese.remaining_quantity <= 0:
            raise APIException(f"No remaining prizez for prize: {prize_to_deacrese.name}")
        
        if user_spins.remaining_spins <= 0:
            raise APIException(f"No remaining spins for user: {user_spins.user.name}")
        
        user_spins.update(remaining_spins=(user_spins.remaining_spins-1))
        prize_to_deacrese.update(remaining_quantity=(prize_to_deacrese.remaining_quantity-1))

        userprize= UserPrize.objects.create(**validated_data)
        return userprize
    
    
class ResetUserPasswordCreateSerializer(serializers.ModelSerializer):     
    class Meta:
        model = ResetUserPassword
        fields = ['user', 'create_date', 'expiers_at', 'is_active', 'temp_pass']
        extra_kwargs = {'create_date': {'read_only': True},
                'expiers_at': {'read_only': True},
                'is_active': {'read_only': True},
                'temp_pass': {'read_only': True},
                'user': {'read_only': True},}
        
    def create(self, validated_data):
        future_date_after_8Hours = datetime.now() + timedelta(hours = 8)
        validated_data['expiers_at']=future_date_after_8Hours
        temp_user_pass_details= ResetUserPassword.objects.create(**validated_data)
        request = self.context['request']
        origin_url =request.query_params['url']
        final_url= f'{origin_url}/{temp_user_pass_details.temp_pass}'
        payload = {
            "service_id": "service_5p8yjor",
            "template_id": "contact_form",
            "user_id": "user_5pshcWi7OYESSWV9vH6ko",
            "template_params": {
                "from_name": "Steven Admin",
                "message": f"{final_url}",
                "to_name":validated_data.get('user').name,
                "user_email":validated_data.get('user').email
            }
        }
        r = requests.post('https://api.emailjs.com/api/v1.0/email/send', data=json.dumps(payload), headers = {'Content-type': 'application/json'})
        "Send email with link from the FE with emailjs services"
        return temp_user_pass_details


class ResetUserPasswordSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    password = serializers.CharField(write_only=True)
    user=UserSerializer(read_only=True)
    #james token 25b2a49f9bb20071824c01b5219763740fbe32f5
    class Meta:
        model = ResetUserPassword
        fields = ['user', 'create_date', 'expiers_at', 'is_active', 'temp_pass', 'password']
        extra_kwargs = {'user': {'read_only': True},
                        'create_date': {'read_only': True},
                        'expiers_at': {'read_only': True},
                        'is_active': {'read_only': True},
                        'temp_pass': {'read_only': True},
                        'password': {'min_length': 5}}
        
        
    def update(self, instance, validated_data):
        """Update and return user."""
        new_password=validated_data.pop('password', None)
        if(new_password == None):
            raise APIException(f"No new password enterd")

        user = instance.user 
        if new_password:
            user.set_password(new_password)
            user.save()
        
        validated_data['is_active'] = False
        temp_user_pass_details = super().update(instance, validated_data)
        temp_user_pass_details.save()
        
        return temp_user_pass_details
    