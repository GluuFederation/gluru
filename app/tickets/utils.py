from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from tickets.models import Ticket
from profiles.models import UserProfile
from tickets import constants


def generate_ticket_link(ticket):

    return reverse('view_ticket', kwargs={
        'category': slugify(ticket.get_ticket_category_display()),
        'id': ticket.id,
        'title': slugify(ticket.title)
    })


def product_select_list(product):
    html = '<div class="controls">'
    html += '<select class="select form-control product" id="id_product" name="product">'
    for key, value in constants.PRODUCT:
        if product == key:
            select = True
        else:
            select = False
        html += '<option value="{}" {}>{}</option>'.format(key, "selected" if select else "", value)
    html += '</select>'
    html += '</div>'
    return html

def product_version_select_list(product_version):
    html = '<div class="controls "> <select class="select form-control product_version" id="id_product_version" name="product_version" >'
    for key,value in constants.Product_Version:
        if product_version == key:
            select = True
        else:
            select = False
        html += '<option value="{}" {}>{}</option>'.format(key, "selected" if select else "", value)
    html += '</select> </div>'
    return html

def product_os_version_select_list(product_os_version):
    html = '<div class="controls "> <select class="select form-control product_os_version" id="id_product_os_version"  name="product_os_version" >'
    for key,value in constants.PRODUCT_OS_VERSION:
        if product_os_version == key:
            select = True
        else:
            select = False
        html += '<option value="{}" {}>{}</option>'.format(key, "selected" if select else "", value)
    html += '</select> </div>'
    return html

def gluu_server_version_select_list (gluu_server_version):
    html = '<div class="controls "> <select class="select form-control gluu_server_version" id="id_gluu_server_version" name="gluu_server_version">'
    for key,value in constants.GLUU_SERVER_VERSION:
        if gluu_server_version == key:
            select = True
        else:
            select = False
        html += '<option value="{}" {}>{}</option>'.format(key, "selected" if select else "", value)
    html += '</select> </div>'
    return html


def gluu_os_version_list(gluu_os_version):
    html = '<div class="controls "> <select class="select form-control os_version" id="id_os_version" name="os_version">'
    for key,value in constants.OS_VERSION:
        if gluu_os_version == key:
            select = True
        else:
            select = False
        html += '<option value="{}" {}>{}</option>'.format(key, "selected" if select else "", value)
    html += '</select> </div>'
    return html


def get_last_ticket_data(user):
    try:
        ticket = Ticket.objects.filter(created_by=user).order_by('-id')[:1]
        data = []
        for t in ticket:
            data.append(t.gluu_server_version)
            data.append(t.os_version)
            data.append(t.os_version_name)
            data.append(t.gluu_server_version_comments)
            data.append(t.os_name)
        return data
    except:
        return []


stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

matchwords = ['outage','system outage', 'unavailable', 'dropped', 'not found', 'invalid', 'accessible', 'logging in','gluu server',
              'fixed', 'defined', 'allow', 'service', 'server', 'connect', 'failiure', 'provider', 'request', 'scim','gluu','saml',
              'url', 'update', 'undefiend', 'access management', 'attribute', 'environment', 'ssl', 'ldap','cache','ui','ux','certificate',
              'identity management', 'identity', 'version', 'endpoint', 'not working', 'validate', 'register','fatal','installed','metadata',
              'enable', 'disable', 'application', 'login', 'logout', 'missing', 'reset', 'gateway', 'client', 'api','plugin','oxtrust',
              'userinfo', 'fails', 'flow', 'handle', 'admin', 'authentication', 'redirect', 'repeat', 'script','information','idp',
              'account', 'expire','expired', 'uma', 'oauth', 'token', 'ticket', 'authorization', 'user management', 'error','unable','documentation',
              'username', 'password', 'scope', 'dns', 'public', 'private', 'upgrade', 'ubuntu', 'centOs', 'debian','management',
              'rhel', '3.1.0', '3.0.1', '3.0.2', '2.4.4', '2.4.3', '14.04', '16.02', '6.5', '6.6', '6.7', 'installation',
              'production', 'impaired', 'maintenance', 'customization', 'feature request', '500', '404','ssh', 'issue', 'fault','problem']

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def removeStopwords(wordlist, matchwords):
    return [w for w in wordlist if w in matchwords]

def removeWords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]
