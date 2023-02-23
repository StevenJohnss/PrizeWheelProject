"""
Serializers for the prize API View.
"""

from core.models import Prize
from django.utils.translation import gettext as _

from rest_framework import serializers


class PrizeSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Prize
        fields = ['name','id']
