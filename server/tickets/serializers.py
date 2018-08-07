from rest_framework import serializers
from tickets.models import Ticket, Answer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, valdiated_data):
        ticket = self.context['ticket']

        return Answer.objects.create(
            ticket=ticket,
            **valdiated_data
        )
