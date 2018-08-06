from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^constants/$', views.ConstantsView.as_view()),
]
