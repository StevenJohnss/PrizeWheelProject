"""
Views for the user API.
"""
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from prize.serializers import (
    PrizeSerializer
)
from core.models import Prize


class PrizeViews(generics.ListAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class PrizeCreateViews(generics.CreateAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class PrizedetailViews(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field='id'
