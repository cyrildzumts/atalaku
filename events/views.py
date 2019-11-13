from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event, Category
from events.forms import EventForm, EventCancelForm, CategoryForm, EventSearchForm, TicketForm
from events.event_services import EventService
import logging


logger = logging.getLogger(__name__)


def event_home(request):
    events = EventService.get_events(start=0, end=5)
    page_title = 'Events Home'
    template_name = 'events/event_home.html'
    context = {
        'events': events,
        'page_title': page_title
    }
    return render(request, template_name, context)

# Create your views here.
def events(request):
    events = EventService.get_events()
    page_title = 'Events'
    template_name = 'events/events.html'
    context = {
        'events': events,
        'page_title': page_title
    }
    return render(request, template_name, context)


def event_detail(request, event_uuid=None):
    event = EventService.get_event(event_uuid)
    template_name = 'events/event_detail.html'
    context = {
        'event': event,
        'page_title': 'Event ' + event.name,
        'monitoring': EventService.event_summary(event_uuid)
    }
    return render(request, template_name, context)


@login_required
def event_update(request, event_uuid=None):
    event = get_object_or_404(Event, event_uuid=event_uuid)
    template_name = 'events/event_update.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)


        if event_data:
            logger.debug("Event Update  : Event date %s", event_data)
            event = EventService.event_update(event.pk, **event_data)
            messages.success(request, "The Event has been updated")
            return redirect('events:event-detail', event_uuid=event_uuid)
        else :
            form = EventForm(request.POST, instance=event)
            logger.debug("Event Update  : Event data is None")
            messages.error(request, "The Event could not be updated. Please check your submitted form")
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
    template_name = 'events/event_create.html'
    if request.method == 'POST':
        event_data = EventService.extract_event_data_from_form(request)
        if event_data:
            event, created = EventService.create_event(**event_data)
            if created:
                messages.success(request, "The Event has been created")
                return redirect('events:event-detail', event_uuid=event.event_uuid)
            else :
                messages.error(request, "The Event could not be created. An Event with the same information already exists")
        else :
            messages.error(request, "The Event could not be updated. Please check your submitted form")

    context = {
        'page_title': 'Event Creation',
        'form' : EventForm()

    }
    return render(request, template_name, context)

@login_required
def event_cancel(request, event_uuid=None):
    canceled = EventService.cancel_events(**{'event_uuid':event_uuid})
    if canceled:
        messages.success(request, "The Event has been canceled")
    else :
        messages.error(request, "The Event could not be canceled")
        logger.error("The Event with uuid %s could not be canceled", event_uuid)
    
    return redirect('home')


@login_required
def event_delete(request, event_uuid=None):
    EventService.delete_event(event_uuid)
    
    return redirect('events:event-home')


@login_required
def event_buy_ticket(request, event_uuid=None):
    template_name = "events/buy_ticket.html"
    page_title = "Buy Event Ticket"
    event = EventService.get_event(event_uuid)
    form = TicketForm()
    context = {
        'page_title' : page_title,
        'form' : form,
        'event': event
    }
    logger.debug("Event Ticket Buy View - Event %s", event_uuid)
    if request.method == 'POST':
        form = TicketForm(request.POST)
    elif request.method == 'GET':
        pass
    

    return render(request, template_name, context)

def event_search(request):
    template_name = "events/search.html"
    page_title = "Search"
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
    template_name = "events/category_events.html"
    page_title = (category is not None and (category.name + " Events")) or "Events"
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
        if request.user.is_authenticated:
            messages.error(request, message)
        else :
            messages.error(request, "You must log in before you can use this action")
    
    return redirect('events:event-detail', event_uuid=event.event_uuid)



@login_required
def event_remove_participant(request, event_uuid=None):
    event, removed, message = EventService.remove_event_participant(event_uuid, request.user)
    if removed:
        messages.success(request, message)
    else:
        if request.user.is_authenticated:
            messages.error(request, message)
        else :
            messages.error(request, "You must log in before you can use this action")
    
    return redirect('events:event-detail', event_uuid=event.event_uuid)


@login_required
def event_like(request, event_uuid=None):
    event, added, message = EventService.add_event_as_favorite(event_uuid, request.user)
    if added:
        messages.success(request, message)
    else:
        if request.user.is_authenticated:
            messages.error(request, message)
        else :
            messages.error(request, "You must log in before you can use this action")
    
    return redirect('events:event-detail', event_uuid=event.event_uuid)

@login_required
def event_unlike(request, event_uuid=None):
    event, removed , message = EventService.remove_event_as_favorite(event_uuid, request.user)
    if removed:
        messages.success(request, message)
    else:
        if request.user.is_authenticated:
            messages.error(request, message)
        else :
            messages.error(request, "You must log in before you can use this action")
    
    return redirect('events:event-detail', event_uuid=event.event_uuid)



@login_required
def create_event_category(request):
    form = None
    if request.method == 'POST':
        form = CategoryForm(request.POST.copy())
        if form.is_valid():
            name = form.cleaned_data['name']
            category = EventService.create_category(name)
            if category:
                return redirect('events:event-home')

    if request.method == 'GET':
        form = CategoryForm()
    template_name = 'events/create_category.html'
    context = {
        'page_title' : 'Category Creation',
        'form' : form,
    }

    return render(request, template_name, context)