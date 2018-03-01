from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from search.views import SearchView


urlpatterns = [
    url(
        r'^grappelli/',
        include('grappelli.urls')
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^search/$',
        SearchView.as_view(),
        name='haystack_search'
    ),
    url(
        r'^',
        include('profiles.urls', namespace='profile'),
    ),
    url(
        '',
        include('social.apps.django_app.urls', namespace='social')
    ),
    url(
        r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.png')
    ),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots'
    ),
    url(
        r'^',
        include('tickets.urls')
    ),

]

handler404 = 'main.views.handle_404'
handler500 = 'main.views.handle_500'
