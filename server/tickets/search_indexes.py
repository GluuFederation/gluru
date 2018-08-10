
from haystack import indexes
from tickets.models import Ticket


class TicketIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(
        document=True,
        use_template=True
    )

    status = indexes.CharField(
        model_attr='status'
    )

    os_version = indexes.CharField(
        model_attr='os_version'
    )

    server_version = indexes.CharField(
        model_attr='server_version'
    )

    category = indexes.CharField(
        model_attr='category'
    )

    is_private = indexes.BooleanField(
        model_attr='is_private'
    )

    created_by = indexes.CharField(
        model_attr='created_by'
    )

    created_for = indexes.CharField(
        model_attr='created_for'
    )

    company = indexes.CharField(
        model_attr='company'
    )

    created_at = indexes.DateTimeField(
        model_attr='created_at'
    )

    title_auto = indexes.EdgeNgramField(
        model_attr='title'
    )

    def get_model(self):
        return Ticket

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
