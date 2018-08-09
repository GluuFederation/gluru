import json
import markdown
import os
import base64
import datetime
import re
import urllib2
import cgi
import shutil
from tomd import Tomd
import textile
import string
from itertools import groupby
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q, F
from django.core.files import File
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from django.views.decorators.http import require_GET, require_POST
from django.core.cache import cache
from twilio.rest import Client
from django.http import JsonResponse
from main.utils import log_error, log_crm
from django.views.decorators.csrf import csrf_exempt
from profiles.models import UserProfile, Company

from tickets import forms
from tickets.constants import TICKET_CATEGORY, ISSUE_TYPE, PRODUCT
from tickets.models import (
    Ticket, Category, Answer, TicketDocuments, TicketNotification,TicketProduct,
    TicketAlerts, TicketBlacklist)
from tickets.utils import generate_ticket_link,wordListToFreqDict,sortFreqDict,stopwords,removeWords,removeStopwords,matchwords

from alerts import views as alert

from connectors.sugarcrm.crm_interface import get_support_plan, account_inactive, downgrade_named_user

from search.forms import TicketSearchForm

from bs4 import BeautifulSoup as bsoup


def home(request):
    categories = []

    if cache.get('home_categories') is not None:
        categories = cache.get('home_categories')

    else:
        for c in TICKET_CATEGORY:
            category = Category(c[1])

            category.tickets_no = Ticket.objects.get_active(request.user).filter(
                ticket_category=c[0]).count()

            if category.tickets_no > 0:

                category.tickets = Ticket.objects.get_active(request.user).filter(
                    ticket_category=c[0]).order_by('-date_added')[:5]

                categories.append(category)

        categories = sorted(categories, key=lambda x: x.tickets_no, reverse=True)
        cache.set('home_categories', categories, timeout=settings.CACHE_TIMEOUT)

    return render(request, 'home.html', {'categories': categories,
                                         'search_form': TicketSearchForm})


def tickets_lists(request, category=None):

    try:

        categories = {slugify(c[1]): c for c in TICKET_CATEGORY if c[0]}

        tickets = Ticket.objects.get_active(request.user).filter(
            ticket_category=categories[category][0]).order_by('-date_added')

        category = categories[category][1]

        paginator = Paginator(tickets, settings.TICKETS_PER_PAGE)

        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)

        first = center = last = ''

        if paginator.num_pages >= 10:

            if tickets.number <= 4:
                first = range(1, 6)
                center = []
                last = [paginator.num_pages]
            if tickets.number > 4 and tickets.number <= tickets.paginator.num_pages - 4:
                first = range(1, 3)
                center = [tickets.number - 1, tickets.number, tickets.number + 1]
                last = [paginator.num_pages - 1, paginator.num_pages]
            if tickets.number > tickets.paginator.num_pages - 4:
                first = range(1, 3)
                center = []
                last = range(paginator.num_pages - 4, paginator.num_pages + 1)

        categories = [c for c in TICKET_CATEGORY if c[0]]

        return render(request, 'tickets/list.html', {
            'tickets': tickets,
            'category': category,
            'categories': categories,
            'page': 'list',
            'pager': {
                'first': first, 'center': center, 'last': last,
                'per_page_init': (page - 1) * 10,
                'per_page_fin': (page * 10, paginator.count)[paginator.count < page * 10]
            },
        })
    except KeyError:
        return redirect(reverse('home'))


def view_ticket(request, category=None, title=None, id=None):

    try:
        ticket = Ticket.objects.get(id=id, is_deleted=False)
        ticket.visits += 1
        keyword_array=[]
        wordstring = ticket.title.lower()
        wordstring += ticket.description.lower()
        wordlist = wordstring.split()
        wordfreq = [wordlist.count(w) for w in wordlist] # a list comprehension


        newwordlist = removeStopwords(wordlist, matchwords)
        dictionary = wordListToFreqDict(newwordlist)
        sorteddict = sortFreqDict(dictionary)
        for s in sorteddict:
            keyword_array.append((str(s[1])))

        ticket.meta_keywords= sorteddict
        ticket.save()
        products= TicketProduct.objects.filter(ticket_id=id)
    except ObjectDoesNotExist:

        messages.error(request, _('Sorry, but this ticket does not exist.'))
        return redirect(reverse('home'))


    if not request.user.is_authenticated() and (ticket.is_private or request.method == 'POST'):

        return redirect(
            '{}?next={}'.format(
                reverse('profile:authorize'),
                generate_ticket_link(ticket)
            )
        )

    if request.user.is_authenticated() and not ticket.has_view_permission(request.user):

        messages.error(request, _(
            'You are not authorized to view this ticket. ' +
            'If you think this is a mistake, please email support@gluu.org.'
        ))

        return redirect(reverse('home'))

    answers_filters = [Q(ticket=ticket) & Q(is_deleted=False)]

    if request.user.is_anonymous():

        answers_filters.extend([
            Q(privacy='public') | (Q(privacy='inherit') & Q(ticket__is_private=False))
        ])

    elif not request.user.is_admin:

        if request.user.is_named:

            clients = Company.objects.filter(
                clients__is_deleted=False,
                clients__partner=request.user.company_association
            )

        else:

            clients = []

        answers_filters.extend([
            (Q(privacy='public') | (Q(privacy='inherit') & Q(ticket__is_private=False))) |
            Q(created_by=request.user) |
            (Q(ticket__created_by=request.user) & Q(ticket__created_for=None)) |
            Q(ticket__created_for=request.user) |
            Q(ticket__company_association=request.user.company_association) |
            Q(ticket__company_association__in=clients)
        ])

    answers = Answer.objects.filter(*answers_filters)

    documents = ticket.ticket_documents.filter(is_deleted=False)

    ticket_form = forms.TicketInlineForm(instance=ticket)

    is_alerts_assigned = False

    if request.user.is_authenticated():

        is_alerts_assigned = TicketAlerts.objects.filter(ticket=ticket, user=request.user).exists()

    answer_form = None

    if request.method == 'GET':

        if request.user.is_authenticated():

            if request.user.is_basic:
                answer_form = forms.UserAnswerForm(
                    user=request.user, ticket=ticket)

            elif request.user.is_named:
                answer_form = forms.NamedUserAnswerForm(
                    user=request.user, ticket=ticket)

            else:
                answer_form = forms.StaffAnswerForm(user=request.user, ticket=ticket)

    elif request.method == 'POST':

        if request.user.is_basic:

            answer_form = forms.UserAnswerForm(
                request.POST, user=request.user, ticket=ticket)

        elif request.user.is_named:

            answer_form = forms.NamedUserAnswerForm(
                request.POST, request.FILES, user=request.user, ticket=ticket)

        else:

            answer_form = forms.StaffAnswerForm(
                request.POST, request.FILES, ticket=ticket
            )

        if answer_form.is_valid():

            if (answer_form.cleaned_data.get('close_ticket') and
               ticket.has_edit_permission(request.user)):
                ticket.status = 'closed'

            if 'status' in answer_form.changed_data:
                ticket.status = answer_form.cleaned_data.get('status')

            elif request.user.is_admin and ticket.status in ['new', 'assigned']:
                ticket.status = 'inprogress'

            if 'assigned_to_answer' in answer_form.changed_data:
                ticket.assigned_to = answer_form.cleaned_data.get('assigned_to_answer')

            elif not ticket.assigned_to and request.user.is_admin:
                ticket.assigned_to = request.user

            answer = answer_form.save(commit=False)
            full_answer =  answer.answer
            answer_without_script = full_answer.replace("<script>","<pre>")
            answer_without_script = answer_without_script.replace("</script>","</pre>")
            answer_without_script = answer_without_script.replace("script/src","")
            answer_without_script = answer_without_script.replace("onerror=","")
            answer_without_script = answer_without_script.replace("alert","")
            answer.answer = answer_without_script
            answer.ticket = ticket
            answer.created_by = request.user
            answer.save()

            if request.POST.get("answer"):
                ans= request.POST.get("answer")
                tagged_users = re.findall(r'@[\w\.-]+', ans)
                if tagged_users:
                    for tagged_user in tagged_users:
                        try:
                            name = tagged_user.replace('@','').split('.')
                            users= UserProfile.objects.filter(first_name__icontains=name[0],last_name__icontains=name[1])
                            if users:
                                for user in users:
                                    alert.notify_tagged_staff_member(answer, user)
                        except:
                            pass
            if request.FILES:
                for f in request.FILES:
                    TicketDocuments.objects.create(
                        file=request.FILES[f], created_by=request.user, answer=answer
                    )

            ticket.support_plan = get_support_plan(request.user)
            if not ticket.support_plan:
                ticket.support_plan = {}

            ticket.answers_no = F('answers_no') + 1

            ticket.save(user=request.user)

            if 'assigned_to' in ticket.diff and ticket.assigned_to:

                alert.notify_ticket_assigned(ticket=ticket, user=request.user)

            alert.notify_new_answer(answer=answer, send_copy=answer.send_copy)

            if request.user not in [ticket.owned_by, ticket.assigned_to]:
                TicketAlerts.objects.update_or_create(ticket=ticket, user=request.user)

            messages.success(request, _('The answer has been posted!'))

            return redirect('{}#at{}'.format(generate_ticket_link(ticket), answer.id))

    subscribed_user_count = 1

    if ticket.assigned_to:
        subscribed_user_count += 1

    subscriber_company = ticket.owned_by.get_company()
    try:
        subscribed_user=UserProfile.objects.filter(company=subscriber_company, receive_all_notifications = True).exclude(email=ticket.owned_by.email)

    except ObjectDoesNotExist:

        subscribed_user = {}

    if subscribed_user:
        for user in subscribed_user:
            subscribed_user_count += 1
    try:
        ticket_alerts = TicketAlerts.objects.select_related('user').filter(ticket=ticket).exclude(user=ticket.assigned_to)
    except ObjectDoesNotExist:
        ticket_alerts = {}

    if ticket_alerts:
        for ticket_alert in ticket_alerts:
            subscribed_user_count +=1

    return render(request, 'tickets/view.html', {
        'ticket': ticket,
        'products': products,
        'keyword_array': keyword_array,
        'answers': answers,
        'page': 'view',
        'documents': documents,
        'is_alerts_assigned': is_alerts_assigned,
        'answer_form': answer_form,
        'ticket_form': ticket_form,
        'category': category,
        'has_edit_rights': ticket.has_edit_permission(request.user),
        'has_view_rights': ticket.has_view_permission(request.user),
        'has_delete_rights': ticket.has_delete_permission(request.user),
        'user_organization':request.user.get_company() if request.user.is_authenticated() else "",
        'organization': ticket.created_by.get_company(),
        'subscribed_user_count': subscribed_user_count,
        'subscribed_user': subscribed_user,
        'ticket_alerts': ticket_alerts
    })


def get_ticket_form(user):

    if user.is_basic:
        return forms.UserTicketForm

    elif user.is_named:

        clients = Company.objects.filter(
            clients__is_deleted=False,
            clients__partner=user.company_association
        )

        if len(clients):
            return forms.PartnerTicketForm
        else:
            return forms.NamedUserTicketForm

    else:
        return forms.StaffTicketForm


@login_required
def add_ticket(request):
    ticket_form = get_ticket_form(request.user)
    if ticket_form == forms.PartnerTicketForm:
        clients = Company.objects.filter(
            clients__is_deleted=False,
            clients__partner=request.user.company_association
        )

        if request.method == 'GET':
            ticket_form = forms.PartnerTicketForm(clients, request.user)

        elif request.method == 'POST':
            ticket_form = forms.PartnerTicketForm(clients, request.user, request.POST)

    else:
        if request.method == 'GET':
            ticket_form = ticket_form(request.user)


        elif request.method == 'POST':
            ticket_form = ticket_form(request.user, request.POST)

    if request.method == 'POST':

        if ticket_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user
            ticket.created_for = ticket_form.cleaned_data.get('created_for', None)

            if ticket.owned_by.company_association:
                ticket.company_association = ticket.owned_by.company_association

            if ticket.created_for:
                ticket.support_plan = get_support_plan(ticket.created_for)
            else:
                ticket.support_plan = get_support_plan(request.user)
            if not ticket.support_plan:
                ticket.support_plan = {}
            ticket_description =  ticket.description
            description_without_script = ticket_description.replace("<script>","<pre>")
            description_without_script = description_without_script.replace("</script>","</pre>")
            description_without_script = description_without_script.replace("script/src","")
            description_without_script = description_without_script.replace("onerror=","")
            description_without_script = description_without_script.replace("alert","")
            ticket.description = description_without_script
            ticket.save()


            if request.POST.get('product'):
                product = request.POST.getlist('product')
                product_version = request.POST.getlist('product_version')
                product_os_version = request.POST.getlist('product_os_version')
                product_os_version_name = request.POST.getlist('product_os_version_name')
                list_length = len(product)
                if request.POST.getlist('ios_version_name'):
                    ios_version_name=request.POST.getlist('ios_version_name')
                for i in range(list_length):
                    if product_os_version[i] == "Both":
                        TicketProduct.objects.create(product=product[i],product_version=product_version[i],
                                              product_os_version=product_os_version[i],product_os_version_name=product_os_version_name[i],ios_version_name=ios_version_name[i],ticket=ticket)
                    else:
                        TicketProduct.objects.create(product=product[i],product_version=product_version[i],
                                              product_os_version=product_os_version[i],product_os_version_name=product_os_version_name[i],ticket=ticket)

            if ticket.support_plan and (ticket.issue_type == 'outage' or ticket.issue_type == 'impaired'):
                TicketNotification.objects.create(
                    ticket=ticket,
                    is_txt_sent=0,
                    is_call_sent=0
                )
            for issue in ISSUE_TYPE:
                if issue[0] == ticket.issue_type:
                    ticket.issue_type = issue[1]

            alert.notify_new_ticket(ticket=ticket, send_copy=ticket.send_copy)

            if ticket.assigned_to:

                ticket.status = 'assigned'
                ticket.save(user=request.user)
                alert.notify_ticket_assigned(ticket=ticket, user=request.user)

            else:
                if request.user.is_admin:
                    ticket.assigned_to = request.user
                    ticket.status='assigned'
                    ticket.save(user=request.user)
                    alert.notify_ticket_assigned(ticket=ticket, user=request.user)

            messages.success(request, _('Your ticket has been saved!'))
            messages.warning(request, _('You will receive emails with all ticket changes!'))

            if request.POST.get('file_field'):
                files = request.POST.getlist('file_field')
                file_source = request.POST.getlist('file_src')
                file_list_length=len(files)

                for x in range(file_list_length):
                     TicketDocuments.objects.create(
                        file=File(open(settings.MEDIA_ROOT+'/'+str(request.user.id)+'/'+str(files[x]),'r')),
                        created_by=request.user,
                        ticket=ticket,
                        file_src = file_source[x]
                    )
                shutil.rmtree(settings.MEDIA_ROOT+'/'+str(request.user.id))
            return HttpResponseRedirect(generate_ticket_link(ticket))

        else:
            messages.error(request, _('Error saving the ticket!'))

    return render(
        request,
        'tickets/add.html',
        {'ticket_form': ticket_form,
         'page': 'add'}
    )


@login_required
@csrf_exempt
def add_files(request):

    files = request.FILES.getlist('qqfile')
    files_list_length=len(files)
    for f in range(files_list_length):
        handle_uploaded_file(files[f], str(files[f]),request.user)
    return HttpResponse(json.dumps({'success': 'true'}),
                content_type='application/json')


def handle_uploaded_file(file, filename, user):
    if not os.path.exists(settings.MEDIA_ROOT+"/"+str(user.id)+'/'):
        os.mkdir(settings.MEDIA_ROOT+"/"+str(user.id)+'/')
    filename= filename.replace(' ', '_')
    with open(settings.MEDIA_ROOT+"/"+str(user.id)+'/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def gluu_default_values(request):

    user_id = request.POST.get("user_id")

    ticket = Ticket.objects.filter(created_for=user_id).order_by('-id')[:1]
    data = []

    for t in ticket:
        data.append(t.gluu_server_version)
        data.append(t.os_version)
        data.append(t.os_version_name)
        data.append(t.gluu_server_version_comments)
    return HttpResponse(json.dumps({'success': 'true', 'data':data, }),
                  content_type='application/json')

def populate_ticket_data(request):

    ticket_id = request.POST.get("ticket_id")
    file_src_array = []
    file_name_array = []
    try:

        attachments=TicketDocuments.objects.filter(ticket_id=ticket_id)

    except ObjectDoesNotExist:

        messages.error('No attachment found')

    if attachments:
        for attachment in attachments:

            file_with_path = str(attachment.file).split('/')
            file_name = file_with_path[3]
            file_src_array.append(attachment.file_src)
            file_name_array.append(file_name)
            file = File(open(settings.MEDIA_ROOT+'/'+str(attachment.file),'r'))
            handle_uploaded_file(file,file_name,request.user)


    return HttpResponse(json.dumps({'success': 'true','file_src':file_src_array, 'file_name':file_name_array }),
                  content_type='application/json')



def read_file(filename):
    with open(filename, 'rb') as f:
        file = f.read()
    return file

@login_required
def edit_ticket(request, id):

    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket not found'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if not ticket.has_edit_permission(request.user):
        messages.error(request, _('You are not authorized to edit this ticket!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    # instantiate ticket form
    ticket_form = get_ticket_form(request.user)

    if ticket_form == forms.PartnerTicketForm:
        clients = Company.objects.filter(
            clients__is_deleted=False,
            clients__partner=request.user.company_association
        )

        if request.method == 'GET':
            ticket_form = forms.PartnerTicketForm(clients, request.user, instance=ticket)

        elif request.method == 'POST':
            ticket_form = forms.PartnerTicketForm(clients, request.user, request.POST, instance=ticket)

    else:
        if request.method == 'GET':
            ticket_form = ticket_form(request.user, instance=ticket)

        elif request.method == 'POST':
            ticket_form = ticket_form(request.user ,request.POST,instance=ticket)

    if request.method == 'POST':

        if ticket_form.is_valid():

            ticket = ticket_form.save(commit=False)

            if ticket_form.cleaned_data.get('created_for', None):
                ticket.created_for = ticket_form.cleaned_data.get('created_for')

            if ticket.owned_by.company_association:
                ticket.company_association = ticket.owned_by.company_association

            ticket.support_plan = get_support_plan(request.user)
            if not ticket.support_plan:
                ticket.support_plan = {}

            ticket.save(user=request.user)


            TicketProduct.objects.filter(ticket=ticket).delete()

            if request.POST.get('product'):
                product = request.POST.getlist('product')
                product_version = request.POST.getlist('product_version')
                product_os_version = request.POST.getlist('product_os_version')
                product_os_version_name = request.POST.getlist('product_os_version_name')
                list_length = len(product)
                if request.POST.getlist('ios_version_name'):
                    ios_version_name=request.POST.getlist('ios_version_name')
                for i in range(list_length):
                    if product_os_version[i] == "Both":
                        TicketProduct.objects.update_or_create(product=product[i],product_version=product_version[i],
                                              product_os_version=product_os_version[i],product_os_version_name=product_os_version_name[i],ios_version_name=ios_version_name[i],ticket=ticket)
                    else:
                        TicketProduct.objects.update_or_create(product=product[i],product_version=product_version[i],
                                              product_os_version=product_os_version[i],product_os_version_name=product_os_version_name[i],ticket=ticket)

            if 'assigned_to' in ticket.diff and ticket.assigned_to:

                if ticket.status == 'new':
                    ticket.status = 'assigned'
                    ticket.save(user=request.user)

                alert.notify_ticket_assigned(ticket=ticket, user=request.user)

            messages.success(request, _('The ticket has been changed!'))


            if request.POST.get('uploaded_files') == "":
                files = TicketDocuments.objects.filter(ticket=ticket)
                for f in files:
                    os.remove(settings.MEDIA_ROOT+'/'+str(f.file))
                    TicketDocuments.objects.filter(ticket=ticket, file=f.file).delete()

            if request.POST.get('uploaded_files') != "":
                uploaded_files = request.POST.getlist('uploaded_files')
                list_length = len(uploaded_files)
                files_with_path=[]
                for z in range(list_length):
                    files_with_path.append('protected/ticket/'+str(ticket.id)+"/"+str(uploaded_files[z]))

                files = TicketDocuments.objects.filter(ticket=ticket)
                for f in files:
                    if not str(f.file) in files_with_path:
                        os.remove(settings.MEDIA_ROOT+'/'+str(f.file))
                        TicketDocuments.objects.filter(ticket=ticket, file=f.file).delete()

            if request.POST.get('file_field'):
                files = request.POST.getlist('file_field')
                file_source = request.POST.getlist('file_src')
                file_list_length=len(files)
                for x in range(file_list_length):
                    TicketDocuments.objects.create(
                        file=File(open(settings.MEDIA_ROOT+'/'+str(request.user.id)+'/'+str(files[x]),'r')),
                        created_by=request.user,
                        ticket=ticket,
                        file_src = file_source[x]
                    )
                shutil.rmtree(settings.MEDIA_ROOT+'/'+str(request.user.id))

            return HttpResponseRedirect(generate_ticket_link(ticket))

        else:

            messages.error(request, _('Error saving the ticket!'))

    documents = ticket.ticket_documents.filter(is_deleted=False).count()

    return render(request, 'tickets/edit.html', {
        'ticket_form': ticket_form,
        'ticket': ticket,
        'documents': documents,
        'page': 'edit'
    })


@require_POST
@login_required
def edit_ticket_inline(request, id):

    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket not found'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if not ticket.has_edit_permission(request.user):

        messages.error(request, _('You are not authorized to edit this ticket!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    ticket_form = forms.TicketInlineForm(request.POST, instance=ticket)

    if ticket_form.is_valid():

        ticket = ticket_form.save(commit=False)

        ticket.support_plan = get_support_plan(request.user)
        if not ticket.support_plan:
            ticket.support_plan = {}

        ticket.save(user=request.user)


        if 'assigned_to' in ticket.diff and ticket.assigned_to:

            if ticket.status == 'new':
                ticket.status = 'assigned'
                ticket.save(user=request.user)

            alert.notify_ticket_assigned(ticket=ticket, user=request.user)

        messages.success(request, _('The ticket has been updated!'))

    else:
        messages.error(request, _('Ticket could not be updated!'))

    return HttpResponseRedirect(generate_ticket_link(ticket))



@login_required
def history_ticket(request, title, id):
    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket not found'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if not ticket.has_edit_permission(request.user):

        messages.error(request, _('You are not autorized to see requested page!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    history = ticket.ticket_history.all()

    return render(request, 'tickets/history.html', {
        'ticket': ticket,
        'history': history,
        'page': 'history'
    })


def autocomplete_users(request):
    query = request.GET.get('q')
    result= UserProfile.objects.filter(is_active=True, crm_type__in=['staff', 'admin', 'manager'])
    suggestions = {}
    for row in result:
        username= row.first_name+' '+row.last_name
        id= str(row.id)+","+username
        suggestions.update({id:username})
    return HttpResponse(json.dumps({
            'suggestions': suggestions
        }), content_type='application/json')

@login_required
def delete_ticket(request, id):
    ''' Only allowed for admin or creator '''

    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('We could not find that ticket.'))
        log_error('Failed to delete ticket #{}'.format(id))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if not ticket.has_delete_permission(request.user):

        messages.error(request, _('You are not autorized to delete!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    ticket.is_deleted = True
    ticket.save(user=request.user)

    answers = ticket.ticket_answers.all()

    for a in answers:
        a.is_deleted = True
        a.save()

    messages.success(request, _('The ticket has been deleted!'))

    if request.user.is_admin:
        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'all-tickets'}))
    else:
        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))


@login_required
def activate_ticket(request, id):
    ''' Only allowed for admin or creator '''

    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('We could not find that ticket.'))
        log_error('Failed to delete ticket #{}'.format(id))

    ticket.is_deleted = False
    ticket.save(user=request.user)

    answers = ticket.ticket_answers.all()

    for a in answers:
        a.is_deleted = False
        a.save()

    results = {
            "success": 1
        }
    return JsonResponse(results, status=200)


@login_required
def close_ticket(request, id):

    try:
        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket not found'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if not ticket.has_edit_permission(request.user):

        messages.error(request, _('You are not autorized to edit this ticket!'))

        return HttpResponseRedirect(
            reverse('profile:dashboard', kwargs={'page_type': 'my-tickets'}))

    if ticket.status != 'closed':

        ticket.status = 'closed'
        ticket.save(user=request.user)
        messages.success(request, _('The ticket has been closed!'))

    else:

        if not request.user.is_basic:

            last_status = ticket.ticket_history.filter(field_name='status').last().before_value

            if last_status:
                ticket.status = last_status
                ticket.support_plan = get_support_plan(request.user)
                if not ticket.support_plan:
                    ticket.support_plan = {}

            else:
                ticket.status = 'new'
                ticket.support_plan = get_support_plan(request.user)
                if not ticket.support_plan:
                    ticket.support_plan = {}


            ticket.save(user=request.user)
            alert.notify_ticket_reopened(ticket=ticket, user=request.user)
            messages.success(request, _('The ticket has been reopened!'))

    return HttpResponseRedirect(generate_ticket_link(ticket))


@login_required
@require_POST
def ticket_assign_inline(request):

    af = forms.AssignInline(request.POST)

    if af.is_valid():

        try:
            ticket = Ticket.objects.get(id=af.cleaned_data['tid'])
            assigned_to = UserProfile.objects.get(id=af.cleaned_data['uid'])

        except ObjectDoesNotExist:

            return HttpResponse(json.dumps(
                {'status': 'error', 'msg': _('Ticket or Assignee not found')}),
                content_type='application/json')

        if not ticket.has_edit_permission(request.user):

            return HttpResponse(json.dumps(
                {'status': 'error', 'msg': _('Permission denied')}),
                content_type='application/json')

        ticket.assigned_to = assigned_to

        if ticket.created_for:
            ticket.support_plan = get_support_plan(ticket.created_for)
        else:
            ticket.support_plan = get_support_plan(request.user)
        if not ticket.support_plan:
            ticket.support_plan = {}

        ticket.save(user=request.user)

        if 'assigned_to' in ticket.diff and ticket.assigned_to:

            if ticket.status == 'new':
                ticket.status = 'assigned'
                ticket.save(user=request.user)

            alert.notify_ticket_assigned(ticket=ticket, user=request.user)

        return HttpResponse(json.dumps({
            'status': 'success',
            'msg': 'Staff {} has been assigned!'.format(assigned_to.get_full_name())}),
            content_type='application/json'
        )

    else:
        return HttpResponse(json.dumps(
            {'status': 'error', 'msg': _('Invalid data')}),
            content_type='application/json')


@require_POST
@login_required
def ticket_add_alert_inline(request, id):

    try:

        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        return HttpResponse(json.dumps(
            {'status': 'error', 'msg': _('Ticket not found')}),
            content_type='application/json')

    if not ticket.has_view_permission(request.user):

        return HttpResponse(json.dumps(
            {'status': 'error', 'msg': _('Permission denied')}),
            content_type='application/json')

    alert, created = TicketAlerts.objects.update_or_create(
        ticket=ticket, user=request.user)

    if created:

        msg_html = '<span class="glyphicon glyphicon-ban-circle"></span> Remove me from alerts'
        msg = _('You will receive alerts when the ticket will be updated!')

    else:
        alert.delete()
        msg_html = '<span class="glyphicon glyphicon-envelope"></span> Send me alerts'
        msg = _('You will no longer receive alerts when the ticket is updated!')

    return HttpResponse(json.dumps({
        'status': 'success',
        'msg': msg,
        'msg_html': msg_html}),
        content_type='application/json'
    )


@require_GET
@login_required
def ticket_add_alert(request, id):

    try:

        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket does not exist.'))
        return redirect(reverse('home'))

    if not ticket.has_view_permission(request.user):

        messages.error(request, _('Ticket does not exist.'))
        return redirect(reverse('home'))

    alert, created = TicketAlerts.objects.update_or_create(
        ticket=ticket, user=request.user)

    if created:
        messages.success(request, _('You will receive alerts when the ticket will be updated!'))

    else:
        alert.delete()
        messages.success(request, _('You will no longer receive alerts when the ticket is updated!'))

    return HttpResponseRedirect(generate_ticket_link(ticket))


@require_GET
@login_required
def blacklist_ticket(request, id):

    try:

        ticket = Ticket.objects.get(id=id)

    except ObjectDoesNotExist:

        messages.error(request, _('Ticket does not exist.'))
        return redirect(reverse('home'))

    if not ticket.has_view_permission(request.user):

        messages.error(request, _('Ticket does not exist.'))
        return redirect(reverse('home'))

    blacklist_entry, created = TicketBlacklist.objects.update_or_create(
        ticket=ticket, user=request.user)

    messages.success(request, _('You will no longer receive idle reminders concerning this ticket'))

    return HttpResponseRedirect(generate_ticket_link(ticket))


@require_POST
@login_required
def delete_files_inline(request, id):
    ''' Only allowed for owner '''

    try:
        doc = TicketDocuments.objects.get(id=id, is_deleted=False, created_by=request.user)

    except:

        return HttpResponse(json.dumps({
            'status': 'error',
            'msg': _('Document was not found or you don\'t have the right to delete it.')}),
            content_type='application/json')

    doc_file = doc.file.path
    os.remove(doc_file)

    try:
        os.rmdir(os.path.dirname(doc_file))
    except:
        pass

    doc.delete()

    return HttpResponse(json.dumps({
        'status': 'success', 'msg': _('The document has been deleted!')}),
        content_type='application/json')


@require_GET
@login_required
def retrieve_support_plan(request, user_id):

    if not request.user.is_admin:
        return HttpResponse(json.dumps({}), content_type='application/json')

    user = UserProfile.objects.get(id=user_id)

    if user.is_basic:
        return HttpResponse(json.dumps({}), content_type='application/json')


    support_plan = get_support_plan(user)

    if not support_plan:

        if user.is_admin:

            support_plan={"support_plan":"Staff"}

            return HttpResponse(
                json.dumps(support_plan),
                content_type='application/json'
            )
        else:
            return HttpResponse(json.dumps({}), content_type='application/json')

    if support_plan['managed_service'] == 1:
        support_plan['managed_service'] = 'Yes'

    if type(support_plan['renewal_date']) is datetime.date:
        support_plan['renewal_date'] = support_plan['renewal_date'].strftime('%m/%d/%y')

    if type(support_plan['start_date']) is datetime.date:
        support_plan['start_date'] = support_plan['start_date'].strftime('%m/%d/%y')

    for k in support_plan.keys():
        if not support_plan[k] or support_plan[k] == 'None':
            support_plan.pop(k, None)

    return HttpResponse(
        json.dumps(support_plan),
        content_type='application/json'
    )


@login_required
@require_GET
def get_answer_inline(request, id):

    try:

        answer = Answer.objects.get(id=int(id))

    except ObjectDoesNotExist:

        return HttpResponse(
            json.dumps({'status': 'error', 'msg': _('Answer not found')}),
            content_type='application/json')

    if request.user.is_admin or answer.created_by == request.user:

        return HttpResponse(
            json.dumps({'status': 'success', 'html': answer.answer}),
            content_type='application/json'
        )

    return HttpResponse(
        json.dumps({'status': 'error', 'msg': _('Permission denied')}),
        content_type='application/json'
    )


@login_required
@require_POST
def edit_answer_inline(request):
    ''' Only allowed for admin or creator '''

    answer_form = forms.AnswerInline(request.POST)

    if answer_form.is_valid():

        try:
            answer_id = answer_form.cleaned_data['id']
            answer = Answer.objects.get(id=answer_id)

        except ObjectDoesNotExist:

            return HttpResponse(
                json.dumps({'status': 'error', 'msg': _('Answer not found.')}),
                content_type='application/json'
            )

        if request.user.is_admin or answer.created_by == request.user:

            answer.answer = answer_form.cleaned_data['answer']
            answer.save()

            return HttpResponse(json.dumps({
                'status': 'success',
                'html': markdown.markdown(
                    answer.answer,
                    safe_mode='escape',
                    extensions=['markdown.extensions.fenced_code'])}),
                content_type='application/json')

    return HttpResponse(json.dumps(
        {'status': 'error', 'msg': _('Permission denied')}),
        content_type='application/json'
    )


@login_required
def delete_answer_inline(request, id):
    ''' Only allowed for admin or creator '''

    try:
        answer = Answer.objects.get(id=int(id))

    except ObjectDoesNotExist:

        return HttpResponse(
            json.dumps({'status': 'error', 'msg': _('Answer not found')}),
            content_type='application/json'
        )

    if request.user.is_admin or answer.created_by == request.user:

        answer.delete()
        answer.ticket.answers_no = F('answers_no') - 1
        answer.ticket.save(user=request.user)

        answer.ticket.ticket_history.create(
            created_by=request.user,
            field_name='answer',
            before_value='Answer by {}'.format(answer.created_by),
            after_value='Deleted'
        )

        return HttpResponse(
            json.dumps({'status': 'success', 'msg': _('The answer has been deleted')}),
            content_type='application/json'
        )

    return HttpResponse(json.dumps(
        {'status': 'error', 'msg': _('Permission denied')}),
        content_type='application/json'
    )


@login_required
def retrieve_company_members_inline(request, company_id):

    if request.user.is_basic:
        return HttpResponse(json.dumps({}), content_type='application/json')

    try:
        users = UserProfile.objects.filter(
            is_active=True,
            company_association__id=company_id
        )

        user_dict = {}

        for user in users:
            user_dict[user.id] = user.get_full_name()

        return HttpResponse(
            json.dumps({'status': 'success', 'users': user_dict}),
            content_type='application/json'
        )

    except Exception as e:
        log_error('Error Retrieving company members: {}'.format(e))
        return HttpResponse(json.dumps({}), content_type='application/json')

@login_required
def get_related_tickets(request):
    words_list=[]
    query = request.GET.get('q', '').strip()
    split_query= request.GET.get('q').lower().split()
    keywords = removeWords(split_query, stopwords)
    for word in keywords:
        if len(word) > 2:
            words_list.append(word)

    q = [Q(title__icontains=query) & Q(is_deleted=False) ]#| Q(description__icontains=query)]
    if not request.user.is_authenticated():
        q.append(Q(is_private = False))
    elif request.user.is_authenticated() and request.user.is_basic:
       q.append(Q(is_private = False))
    elif request.user.is_authenticated() and request.user.is_named:
        q.append(Q(is_private = False) | Q(created_by_id=request.user.id) | Q(company_association_id = request.user.company_association_id))
    result = Ticket.objects.filter(*q)[:10]
    title = ['%s' % row.title for row in result]
    link= ['%s' % generate_ticket_link(row) for row in result]
    # description=['%s' % row.description for row in result]
    if len(words_list) >= 1:
        for words in words_list:
            k = [Q(title__icontains=words) & Q(is_deleted=False)]
            if not request.user.is_authenticated():
                k.append(Q(is_private = False))
            elif request.user.is_authenticated() and request.user.is_basic:
                k.append(Q(is_private = False))
            elif request.user.is_authenticated() and request.user.is_named:
                k.append(Q(is_private = False) | Q(created_by_id=request.user.id) | Q(company_association_id = request.user.company_association_id))
            result = Ticket.objects.filter(*k)[:10]
            keyword_title= ['%s' % row.title for row in result]
            keyword_link = ['%s' % generate_ticket_link(row) for row in result]
            # keyword_description= ['%s' % row.description for row in result]
            for key in keyword_title:
                if key not in title:
                    title.append(key)
            for key in keyword_link:
                if key not in link:
                    link.append(key)

    return HttpResponse(json.dumps({
        'title': title,
        'link':link,
    }), content_type='application/json')

@login_required
def populate_related_tickets(request,title):
    try:
        tickets = Ticket.objects.filter(
            title__icontains=title
        )
        paginator = Paginator(tickets, settings.TICKETS_PER_PAGE)

        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)

        first = center = last = ''

        if paginator.num_pages >= 10:

            if tickets.number <= 4:
                first = range(1, 6)
                center = []
                last = [paginator.num_pages]
            if tickets.number > 4 and tickets.number <= tickets.paginator.num_pages - 4:
                first = range(1, 3)
                center = [tickets.number - 1, tickets.number, tickets.number + 1]
                last = [paginator.num_pages - 1, paginator.num_pages]
            if tickets.number > tickets.paginator.num_pages - 4:
                first = range(1, 3)
                center = []
                last = range(paginator.num_pages - 4, paginator.num_pages + 1)

        return render(request, 'tickets/related_tickets.html', {
            'tickets': tickets,
            'title':title,
            'page': 'list',
            'pager': {
                'first': first, 'center': center, 'last': last,
                'per_page_init': (page - 1) * 10,
                'per_page_fin': (page * 10, paginator.count)[paginator.count < page * 10]
            },
        })
    except KeyError:
        return redirect(reverse('home'))



@login_required
def download_attachment(request, file_id):

    try:
        attachment = TicketDocuments.objects.get(id=file_id)

        if attachment.ticket:
            ticket = attachment.ticket
        else:
            ticket = attachment.answer.ticket

        if not ticket.has_view_permission(request.user):
            return redirect(reverse('home'))

        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(smart_str(attachment.file.name))
        response['X-Sendfile'] = os.path.join(settings.MEDIA_ROOT, attachment.file.name)
        response['Content-Length'] = attachment.file.size

        return response

    except ObjectDoesNotExist:
        log_error('Attachment does not exist: {}'.format(file_id))

    raise Http404


@csrf_exempt
def read_mail(request, data=[]):

    if request and request.method == 'POST':

        sender = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        body_without_quotes = request.POST.get('stripped-text', '')
        markdown_body = body_without_quotes.replace("<","")
        # markdown_body = markdown_body.replace(">","")
        encoded_ticket_id = recipient.split("@")
        ticket_id = base64.b32decode(encoded_ticket_id[0])

        user = UserProfile.objects.get(email=sender)
        ticket = Ticket.objects.get(id=ticket_id)
        answer = Answer(created_by=user,ticket_id=ticket_id, answer=markdown_body)
        answer.save()

    if data:
        encoded_ticket_id = data[0].split("@")
        ticket_id = base64.b32decode(encoded_ticket_id[0])
        user = UserProfile.objects.get(email=data[1])
        ticket = Ticket.objects.get(id=ticket_id)
        answer = Answer(created_by=user, ticket_id=ticket_id, answer=data[2])
        answer.save()

    ticket.support_plan = get_support_plan(user)
    ticket.answers_no += 1
    if not ticket.support_plan:
        ticket.support_plan = {}

    if not ticket.assigned_to and user.is_admin:
        ticket.assigned_to = user
    ticket.save()
    alert.notify_new_answer(answer=answer)


    if user not in [ticket.owned_by, ticket.assigned_to]:
        TicketAlerts.objects.update_or_create(ticket=ticket, user=user)

    return HttpResponse('OK')
