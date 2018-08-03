from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_querset(self):
        queryset = self.queryset

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)

        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        
        server_version = self.request.query_params.get('server_version', None)
        if server_version is not None:
            queryset = queryset.filter(server_version=server_version)

        os_version = self.request.query_params.get('os_version', None)
        if os_version is not None:
            queryset = queryset.filter(os_version=os_version)
        return queryset

    # def create(self, request):
    #     pass
    
    def list(self, request):
        serializer = self.serializer_class(self.get_querset(), many=True)
        return Response(serializer.data)
    
    # def retrieve(self, request):
    #     pass

    # def update(self, request):
    #     pass
