from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from events.models import Event, Category
from events.forms import EventForm, EventCancelForm, CategoryForm, EventSearchForm
from events.event_services import EventService, EventTicket
from django.utils.text import gettext_lazy as _
import logging


logger = logging.getLogger(__name__)


def dashboard_home(request):
    event_list = EventService.get_events()
    page_title = 'Events Home'
    template_name = 'dashboard/dashboard.html'
    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 10)
    logger.debug("Events requested page : %s", page)
    logger.debug("Events List - Number of Pages  : %s", paginator.num_pages)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
        logger.debug("Events requested page not an Integer : %s", page)
    except EmptyPage:
        events = None
        logger.debug("Events requested page : %s - Empty page resulted -", page)
    context = {
        'events': events,
        'page_title': page_title
    }
    return render(request, template_name, context)

# Create your views here.
def events(request):
    event_list = EventService.get_events()
    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    page_title = 'Events'
    template_name = 'dashboard/event_list.html'
    context = {
        'events': events,
        'page_title': page_title
    }
    return render(request, template_name, context)


def event_detail(request, event_uuid=None):
    event = EventService.get_event(event_uuid)
    template_name = 'dashboard/event_detail.html'
    context = {
        'event': event,
        'page_title': 'Event ' + event.name,
        'monitoring': EventService.event_summary(event_uuid)
    }
    return render(request, template_name, context)


@login_required
def event_update(request, event_uuid=None):
    event = get_object_or_404(Event, event_uuid=event_uuid)
    template_name = 'dashboard/event_update.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)


        if event_data:
            logger.debug("Event Update  : Event date %s", event_data)
            event = EventService.event_update(event.pk, **event_data)
            messages.success(request, _("The Event has been updated"))
            return redirect('dashboard:event-detail', event_uuid=event_uuid)
        else :
            form = EventForm(request.POST, instance=event)
            logger.debug("Event Update  : Event data is None")
            messages.error(request, _("The Event could not be updated. Please check your submitted form"))
    else :
        form = EventForm(instance=event)
    context = {
        'event': event,
        'page_title': 'Event ' + event.name,
        'form' : form

    }
    return render(request, template_name, context)

@login_required
def event_create(request):
    template_name = 'dashboard/event_create.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)
        if event_data:
            event, created = EventService.create_event(**event_data)
            if created:
                messages.success(request, _("The Event has been created"))
                return redirect('dashboard:event-detail', event_uuid=event.event_uuid)
            else :
                messages.error(request, _("The Event could not be created. An Event with the same information already exists"))
        else :
            messages.error(request, _("The Event could not be updated. Please check your submitted form"))

    context = {
        'page_title': _('Event Creation'),
        'form' : EventForm()

    }
    return render(request, template_name, context)

@login_required
def event_cancel(request, event_uuid=None):
    canceled = EventService.cancel_events(**{'event_uuid':event_uuid})
    if canceled:
        messages.success(request, _("The Event has been canceled"))
    else :
        messages.error(request, _("The Event could not be canceled"))
        logger.error("The Event with uuid %s could not be canceled", event_uuid)
    
    return redirect('dashboard:home')


@login_required
def event_delete(request, event_uuid=None):
    EventService.delete_event(event_uuid)
    
    return redirect('dashboard:home')

def event_search(request):
    template_name = "dashboard/search.html"
    page_title = _("Search")
    context = {
        'page_title' : page_title,
        'events' : None
    }
    if request.method == 'POST':
        form = EventSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = EventService.event_search(query)
            context['events'] = results
            logger.debug("search query for Event finished")
    return render(request, template_name, context)


def event_category_events(request, category_slug=None):
    events, category  = EventService.get_category_events(category_slug)
    template_name = "dashboard/category_events.html"
    page_title = (category is not None and (category.name + " Events")) or _("Events")
    context = {
        'page_title' : page_title,
        'category': category,
        'events' : events
    }
    return render(request, template_name, context)


@login_required
def event_add_participant(request, event_uuid=None):
    event, added, message = EventService.add_event_participant(event_uuid, request.user)
    if added:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('dashboard:event-detail', event_uuid=event.event_uuid)



@login_required
def event_remove_participant(request, event_uuid=None):
    event, removed, message = EventService.remove_event_participant(event_uuid, request.user)
    if removed:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('dashboard:event-detail', event_uuid=event.event_uuid)


@login_required
def create_event_category(request):
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST.copy())
        if form.is_valid():
            name = form.cleaned_data['name']
            category = EventService.create_category(name)
            if category:
                return redirect('dashboard:home')

    if request.method == 'GET':
        form = CategoryForm()
    template_name = 'dashboard/create_category.html'
    context = {
        'page_title' : _('Category Creation'),
        'form' : form,
    }

    return render(request, template_name, context)



@login_required
def event_tickets(request):
    ticket_list = EventTicket.get_events()
    page = request.GET.get('page', 1)
    paginator = Paginator(ticket_list, 1)
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    page_title = _('Tickets')
    template_name = 'dashboard/ticket_list.html'
    context = {
        'ticket': tickets,
        'page_title': page_title
    }
    return render(request, template_name, context)

@login_required
def ticket_detail(request, ticket_uuid=None):
    ticket = EventService.get_ticket(ticket_uuid)
    template_name = 'dashboard/ticket_detail.html'
    context = {
        'ticket': ticket,
        'event' : ticket.event,
        'page_title': _('Ticket')

    }
    return render(request, template_name, context)