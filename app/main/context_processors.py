import requests
import twitter
from lxml import html

from django.core.cache import cache
from django.conf import settings

from main.utils import log_error

requests.packages.urllib3.disable_warnings()


def include_external_info(request):

    tweets = latest_tweet()
    press = latest_press_releases()

    return {
        'tweets': tweets['tweets'],
        'press_releases': press['press_releases'],
    }


def latest_tweet():

    try:
        tweets = cache.get('tweets')

        if tweets:
            return {'tweets': tweets}

        api = twitter.Api(
            consumer_key=settings.CONSUMER_KEY,
            consumer_secret=settings.CONSUMER_SECRET,
            access_token_key=settings.ACCESS_TOKEN,
            access_token_secret=settings.ACCESS_TOKEN_SECRET
        )

        tweets = api.GetUserTimeline(
            screen_name=settings.TWITTER_USER
        )

        if len(tweets) == 0:
            return {'tweets': ''}

        cache.set('tweets', tweets[:2], settings.TWITTER_TIMEOUT)

        return {'tweets': tweets[:2]}

    except Exception as e:
        log_error('Error when retrieving Tweets: {}'.format(e))
        return {'tweets': ''}

def latest_press_releases():

    press_releases = cache.get('press_releases')

    if press_releases:
        return {'press_releases': press_releases}

    try:
        press_content = requests.get(settings.PRESS_RELEASES_URL)
        tree = html.fromstring(press_content.content)
        press_releases = tree.xpath('//div[@class="year-box"][1]//a')[:2]
        cache_press = []

        for p in press_releases:
            cache_press.append({'title': p.text, 'link': p.attrib['href']})

    except Exception as ex:
        log_error(ex)
        return {'press_releases': ''}

    cache.set('press_releases', cache_press, settings.PRESS_RELEASES_TIMEOUT)
    return {'press_releases': cache_press}
