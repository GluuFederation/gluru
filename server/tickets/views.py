from django.shortcuts import render
from rest_framework import viewsets
from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
