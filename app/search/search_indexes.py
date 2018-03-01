from haystack import indexes
from tickets.models import Ticket


class TicketIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    ticket_status = indexes.CharField(model_attr='status')
    ticket_os_version = indexes.CharField(model_attr='os_version', null=True)
    ticket_server_version = indexes.CharField(model_attr='gluu_server_version', null=True)
    ticket_category = indexes.CharField(model_attr='ticket_category')
    is_private = indexes.BooleanField(model_attr='is_private')
    created_by = indexes.IntegerField(model_attr='created_by__id')
    created_for = indexes.IntegerField()
    company = indexes.CharField()
    date_added = indexes.DateTimeField(model_attr='date_added')
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Ticket

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_deleted=False)

    def prepare_company(self, obj):

        company = obj.company_association

        if company:
            company = company.name
        else:
            company = u''

        return company

    def prepare_created_for(self, obj):

        if obj.created_for:
            created_for = obj.created_for.id
        else:
            created_for = -1

        return created_for
