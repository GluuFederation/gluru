import json, hashlib
from nltk.corpus import stopwords

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.cache import cache
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from search.forms import TicketSearchForm
from tickets.utils import generate_ticket_link,wordListToFreqDict,sortFreqDict,stopwords,removeWords,removeStopwords,matchwords

from profiles.models import Company
from tickets.models import Ticket


class SearchView(View):
    template_name = 'search/search.html'
    search_string, category, status, server_version, os_version, active_tab = ('',) * 6
    page = 1
    user = {}

    def get(self, request, *args, **kwargs):
        data = {}
        self.get_params(request)
        user = self.user
        cache_key = self.get_cache_key()
        filters = Q()
        cache.clear()

        if self.get_cache_result(cache_key) is not None:
            data = self.get_cache_result(cache_key)

        else:
            tickets = Ticket.objects.filter(self.get_basic_filters())

            if user.is_anonymous():
                filters.add(Q(is_private=False), Q.OR)

            elif user.is_basic:
                filters.add(Q(is_private=False), Q.OR)
                filters.add(Q(created_by=user.id), Q.OR)

            elif user.is_named:
                filters.add(Q(is_private=False), Q.OR)
                filters.add((Q(created_by=user.id) & Q(created_for=-1)), Q.OR)
                filters.add(Q(created_for=user.id), Q.OR)

                filters.add(Q(company_association=user.company_association.id), Q.OR)

                clients = Company.objects.filter(
                    clients__is_deleted=False,
                    clients__partner=user.company_association
                ).values_list('id', flat=True)

                filters.add(Q(company_association__in=clients), Q.OR)

            tickets = tickets.filter(filters).order_by('date_added')

            data = {
                'most_answered': self.get_top_answered(tickets),
                'most_viewed': self.get_top_viewed(tickets),
                'most_relevant': self.get_most_relevant(tickets),
                'newest': self.get_newest(tickets),
                'all': tickets,
            }
            self.set_cache_result(cache_key, data)

        return render(request, self.template_name, self.get_view_data(data))

    def get_params(self, request):
        self.search_string = request.GET.get('q', '').strip()
        self.category = request.GET.get('category', '').strip()
        self.status = request.GET.get('status', '').strip()
        self.server_version = request.GET.get('server_version', '').strip()
        self.os_version = request.GET.get('os_version', '')
        self.active_tab = request.GET.get('tab', 'newest')
        self.page = int(request.GET.get('page', 1))
        self.user = self.request.user

    def get_basic_filters(self):
        filters = Q()
        if len(self.search_string):
            filters.add((Q(title__icontains=self.search_string) | Q(description__icontains=self.search_string))
                        & Q(is_deleted=False), Q.AND)

        if len(self.category):
            filters.add(Q(ticket_category=self.category), Q.AND)

        if len(self.status):
            filters.add(Q(status=self.status), Q.AND)

        if len(self.server_version):
            filters.add(Q(gluu_server_version=self.server_version), Q.AND)

        if len(self.os_version):
            filters.add(Q(os_version=self.os_version), Q.AND)

        return filters

    def get_view_data(self, data):
        return {
            'tabs': [
                {
                    'title': 'Newest',
                    'target': 'newest',
                },
                {
                    'title': 'Most Relevant',
                    'target': 'relevant',
                },
                {
                    'title': 'Most Answered',
                    'target': 'answered',
                },
                {
                    'title': 'Most Viewed',
                    'target': 'viewed',
                },
            ],
            'tabs_content': [
                {
                    'section': 'newest',
                    'tickets': self.get_paginated_data(data['newest'])
                },
                {
                    'section': 'relevant',
                    'tickets': self.get_paginated_data(data['most_relevant'])
                },
                {
                    'section': 'answered',
                    'tickets': self.get_paginated_data(data['most_answered'])
                },
                {
                    'section': 'viewed',
                    'tickets': self.get_paginated_data(data['most_viewed'])
                },
            ],
            'tickets': self.get_paginated_data(data['all']),
            'active_tab': self.active_tab,
            'query': self.search_string,
            'form': TicketSearchForm(initial={
                'q': self.search_string,
                'category': self.category,
                'status': self.status,
                'server_version': self.server_version,
                'os_version': self.os_version,
            })
        }

    def get_top_answered(self, results):
        try:
            data = []
            for row in results:
                data.append({
                    'answers': row.answers_no,
                    'object': row
                })

            return sorted(data, key=lambda dct: dct['answers'], reverse=True)
        except Exception as e:
            return []

    def get_most_relevant(self, results):
        try:
            data = []
            for row in results:
                data.append({
                    'count': self.get_keyword_strength_count(row),
                    'object': row
                })

            return sorted(data, key=lambda dct: dct['count'], reverse=True)
        except Exception as e:
            return []

    def get_top_viewed(self, results):
        try:
            data = []
            for row in results:
                data.append({
                    'visits': row.visits,
                    'object': row
                })

            return sorted(data, key=lambda dct: dct['visits'], reverse=True)
        except Exception as e:
            return []

    def get_newest(self, results):
        try:
            data = []
            for row in results:
                data.append({
                    'date_added': row.date_added,
                    'object': row
                })

            return sorted(data, key=lambda dct: dct['date_added'], reverse=True)
        except Exception as e:
            return []

    def get_search_keywords(self):
        try:
            stop_words = set(stopwords.words('english'))
            return filter(lambda w: not w in stop_words, self.search_string.split())
        except Exception as e:
            return []

    def get_keyword_strength_count(self, row):
        try:
            keyword_count = 0
            search_keywords = self.get_search_keywords()
            for word in row.title.split():
                if word in search_keywords:
                    keyword_count += 1

            for word in row.description.split():
                if word in search_keywords:
                    keyword_count += 1

            return keyword_count
        except Exception as e:
            return 0

    def get_paginated_data(self, results):
        try:
            paginator = Paginator(results, settings.SEARCH_RESULTS_PER_PAGE)
            try:
                results = paginator.page(self.page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            return results
        except Exception as e:
            return results

    def get_cache_key(self):
        cache_key = "%s~%s~%s~%s~%s" % (
            self.search_string, self.category, self.status, self.os_version, self.server_version
        )
        if self.user.is_anonymous():
            cache_key += "~is_anonymous"
        elif self.user.is_basic:
            cache_key += "~is_basic"
        elif self.user.is_named:
            cache_key += "~is_named"

        return hashlib.md5(cache_key).hexdigest()

    def set_cache_result(self, key, value):
        cache.set(key, value, timeout=settings.CACHE_TIMEOUT)

    def get_cache_result(self, key):
        return cache.get(key)


class TicketLiveSearchAutoCompleteView(View):
    def get(self, request, *args, **kwargs):
        words_list=[]
        query = request.GET.get('q', '').strip()
        split_query= request.GET.get('q').lower().split()
        keywords = removeWords(split_query, stopwords)
        for word in keywords:
            if len(word) > 2:
                words_list.append(word)
        q = [Q(title__icontains=query) & Q(is_deleted=False)|Q(description__icontains=query)]
        if not request.user.is_authenticated():
            q.append(Q(is_private = False))
        elif request.user.is_authenticated() and request.user.is_basic:
           q.append(Q(is_private = False))
        elif request.user.is_authenticated() and request.user.is_named:
            q.append(Q(is_private = False) | Q(created_by_id=request.user.id) | Q(company_association_id = request.user.company_association_id))

        result = Ticket.objects.filter(*q)
        suggestions = ['%s' % row.title for row in result[:5]]
        if len(words_list) >= 1:
            for words in words_list:
                k = [Q(title__icontains=words) & Q(is_deleted=False) ]
                if not request.user.is_authenticated():
                    k.append(Q(is_private = False))
                elif request.user.is_authenticated() and request.user.is_basic:
                    k.append(Q(is_private = False))
                elif request.user.is_authenticated() and request.user.is_named:
                    k.append(Q(is_private = False) | Q(created_by_id=request.user.id) | Q(company_association_id = request.user.company_association_id))
                result = Ticket.objects.filter(*k)
                keyword_suggestions= ['%s' % row.title for row in result[:5]]
                for key in keyword_suggestions:
                    if key not in suggestions:
                        suggestions.append(key)

        return HttpResponse(json.dumps({
            'suggestions': suggestions
        }), content_type='application/json')
