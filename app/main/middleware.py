import pytz

from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone


class TimezoneMiddleware(object):

    def process_request(self, request):

        if request.user.is_authenticated():
            timezone.activate(request.user.timezone)
        else:
            timezone.activate(pytz.timezone('US/Central'))


class ProfileMiddleware(object):

    def process_request(self, request):

        if request.META['PATH_INFO'] == reverse('profile:dashboard', kwargs={'page_type': 'my-profile'}):
            return

        if request.META['PATH_INFO'].startswith('/accept/'):
            return

        if (request.user.is_authenticated() and
                request.user.profile_incomplete and
                request.user.is_basic):

            return HttpResponsePermanentRedirect(reverse('profile:dashboard', kwargs={'page_type': 'my-profile'}))
