from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    TicketViewSet
)

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
