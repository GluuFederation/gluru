from rest_framework import serializers
from tickets.models import Ticket, Answer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'category', 'created_by')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer

    def create(self, valdiated_data):
        ticket = self.context['ticket']

        return Answer.objects.create(
            ticket=ticket,
            **valdiated_data
        )
