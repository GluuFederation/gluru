from rest_framework import viewsets, generics, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from tickets.models import Ticket, Answer
from tickets.serializers import TicketSerializer, AnswerSerializer

from django.db.models import Q


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)

        ticket_status = self.request.query_params.get('status', None)
        if ticket_status is not None:
            queryset = queryset.filter(status=ticket_status)

        server_version = self.request.query_params.get('server', None)
        if server_version is not None:
            queryset = queryset.filter(server_version=server_version)

        os_version = self.request.query_params.get('os', None)
        if os_version is not None:
            queryset = queryset.filter(os_version=os_version)

        search_string = self.request.query_params.get('q', None)
        if search_string is not None:
            queryset = queryset.filter(
                Q(title__icontains=search_string) |
                Q(description__icontains=search_string)
            )

        return queryset

    def create(self, request):
        serializer_data = request.data.get('ticket', {})
        serializer = self.serializer_class(
            data=serializer_data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        try:
            serializer_instance = self.queryset.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound('A ticket with this id does not exist.')

        serializer_data = request.data.get('ticket', {})

        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound('An ticket with this ID does not exist')

        ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(ticket=self.kwargs['ticket_pk'])

    def create(self, request, ticket_pk=None):
        serializer_data = request.data.get('answer', {})
        context = {}

        try:
            context['ticket'] = Ticket.objects.get(pk=ticket_pk)
        except Ticket.DoesNotExist:
            raise NotFound('A ticket with this id does not exist')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, ticket_pk=None, pk=None):
        try:
            serializer_instance = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise NotFound('An answer with this id does not exist.')

        serializer_data = request.data.get('answer', {})

        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, ticket_pk=None, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise NotFound('An answer with this ID does not exist')

        answer.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
