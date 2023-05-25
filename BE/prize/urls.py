"""
URL mappings for the prize app.
"""
from django.urls import (
    path,
    include,
)

# from rest_framework.routers import DefaultRouter

from prize import views


# router = DefaultRouter()
# router.register('prizes', views.PrizeViews)

app_name = 'prize'

urlpatterns = [
    path('prizes/',  views.PrizeViews.as_view(), name='prizes'),
    path('prizes/<int:id>/',  views.PrizedetailViews.as_view(), name='prize-detail'),
    path('create/',  views.PrizeCreateViews.as_view(), name='prize-create'),
]
