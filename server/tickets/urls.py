from django.conf.urls import include, url

from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'tickets', views.TicketViewSet)

tickets_router = routers.NestedSimpleRouter(
    router,
    r'tickets',
    lookup='ticket'
)
tickets_router.register(
    r'answers',
    views.AnswerViewSet,
    base_name='ticket-answers'
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(tickets_router.urls)),
]
