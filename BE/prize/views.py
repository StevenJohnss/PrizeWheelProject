"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from prize.serializers import (
    PrizeSerializer
)
from core.models import Prize


class PrizeViews(generics.ListAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
