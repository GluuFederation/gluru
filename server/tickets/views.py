from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from tickets.models import Ticket, Answer
from tickets.serializers import TicketSerializer, AnswerSerializer
from tickets import constants

from django.db.models import Q


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
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

        server_version = self.request.query_params.get('server_version', None)
        if server_version is not None:
            queryset = queryset.filter(server_version=server_version)

        os_version = self.request.query_params.get('os_version', None)
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
        print(serializer_data)
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

    # def retrieve(self, request):
    #     pass

    def update(self, request):
        pass


class AnswerListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Answer.objects.select_related(
        'ticket'
    )
    serializer_class = AnswerSerializer

    def create(self, request, ticket_id=None):
        data = request.data.get('answer', {})
        context = {}
        try:
            context['ticket'] = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound('A ticket with this id does not exist')

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDestroyAPIView(generics.DestoryAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Answer.objects.all()

    def destroy(self, request, ticket_id=None, answer_id=None):
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            raise NotFound('An answer with this ID does not exist')

        answer.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


# This constants data is over 1Kbytes.
# We can create same constant variable on frontend side for better performance.
# It seems to be a little hard to maintain for duplicate the contant variable.
# But if the constant don't change frequently, it is okay.
# class ConstantsView(APIView):
#     def get(self, request):
#         content = {
#             'serverVersions': constants.GLUU_SERVER_VERSION,
#             'os': constants.OS_VERSION,
#             'issueTypes': constants.ISSUE_TYPE,
#             'categories': constants.ISSUE_CATEGORY,
#             'status': constants.TICKET_STATUS
#         }
#         return Response(content)
