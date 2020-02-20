from django.contrib.auth.models import User
from django.utils.text import slugify, gettext_lazy as _
from events.models import Event, Category, EventTicket
from events.forms import EventForm, EventCancelForm, CategoryForm
from django.db.models import F, Q
import logging
import datetime
import requests
from atalaku import settings


logger = logging.getLogger('events.event_service')

class EventService:

    @staticmethod
    def get_event(event_uuid=None):
        event = None
        try:
            event = Event.objects.get(event_uuid=event_uuid)
        except Event.DoesNotExist as e:
            logger.error("No Event found with uuid {}", event_uuid)
        return event
    
    @staticmethod
    def get_ticket(ticket_uuid=None):
        ticket = None
        try:
            ticket = EventTicket.objects.get(ticket_uuid=ticket_uuid)
        except EventTicket.DoesNotExist as e:
            logger.error("No Event Ticket found with uuid {}", ticket_uuid)
        return ticket

    @staticmethod
    def delete_event(event_uuid=None):
        logger.warn("Deleting Event with uuid {}", event_uuid)
        Event.objects.filter(event_uuid=event_uuid).delete


    @staticmethod
    def get_events(start=None, end=None, **filters):
        events = Event.objects.filter(**filters)[start:end]
        return events

    @staticmethod
    def get_events_published_by_users(start=None, end=None, user=None, **filters):
        events = Event.objects.none()
        if user and hasattr(user, 'published_events'):
            events = user.published_events.all()()[start:end]
        return events

    
    @staticmethod
    def get_favorite_events(start=None, end=None, user=None, **filters):
        events = Event.objects.none()
        if user and hasattr(user, 'favorite_events'):
            events = user.favorite_events.all()[start:end]
        return events

    
    @staticmethod
    def get_event_participants(start=None, end=None, event=None, **filters):
        participants = User.objects.none()
        if event and hasattr(event, 'participants'):
            participants = event.participants.all()[start:end]
        return participants

    @staticmethod
    def is_event_participant(event=None, user=None):
        is_participant = False
        if(user and hasattr(user, 'is_authenticated') and user.is_authenticated and event and hasattr(event, 'participants')):
            is_participant = event.participants.filter(pk=user.pk).exists()
        return is_participant

    @staticmethod
    def is_favorite_event(event=None, user=None):
        is_favorite = False
        if(user and hasattr(user, 'is_authenticated') and user.is_authenticated and event and hasattr(event, 'liked_by')):
            is_favorite = event.liked_by.filter(pk=user.pk).exists()
        return is_favorite
    
    @staticmethod
    def add_event_participant(event_uuid=None, user=None):
        added = False
        event = EventService.get_event(event_uuid)
        message = None
        if event and user and user.is_authenticated:
            if not EventService.is_event_participant(event, user):
                event.participants.add(user)
                message = _("You have been added as participant to this Event")
                logger.info("The User {}  was added as participant to  the Event {}", user.get_full_name(), event.name)
                added = True
            else:
                message = _("You are already a participant to this Event")
                logger.warn("The User {} is participant to  the Event {}", user.get_full_name(), event.name)
        else:
            message = _("The Event was not found in this site")
            logger.error("The Event {} was not found", event_uuid)

        return event, added, message

    @staticmethod
    def remove_event_participant(event_uuid=None, user=None):
        removed = False
        message = None
        event = EventService.get_event(event_uuid)
        if event and user:
            if EventService.is_event_participant(event, user):
                event.participants.remove(user)
                message = "You have been removed as participants to this Event"
                logger.info("The User {}  was removed as participant from the Event {}",  user.get_full_name(), event.name)
                removed = True
            else :
                message = "You can not be removed as participant to this Event. You are not a participant"
                logger.info("The User {}  can  not be removed as participant from the Event {}. He is not a participant",  user.get_full_name(), event.name)
        else:
            message = "The Event was not found in this site"
            logger.error("The Event {} was not found", event_uuid)

        return event, removed, message


    

    @staticmethod
    def add_event_as_favorite(event_uuid=None, user=None):
        added = False
        message = None
        event = EventService.get_event(event_uuid)
        if event and user and user.is_authenticated :
            if not EventService.is_favorite_event(event, user):
                event.liked_by.add(user)
                message = "This Event have been added into your favorite"
                logger.info("The User {}  was adde the Event {} his favorite", user.get_full_name(), event.name)
                added = True
            else:
                message = "This Event is already in your favorite"
                logger.warn("The Event {} is already in the User favorite")
        else:
            message = "The Event was not found in this site"
            logger.error("The Event {} was not found", event_uuid)

        return event, added, message

    @staticmethod
    def remove_event_as_favorite(event_uuid=None, user=None):
        removed = False
        message = None
        event = EventService.get_event(event_uuid)
        if event and user:
            if EventService.is_favorite_event(event, user):
                event.liked_by.remove(user)
                message = "This Event has been removed from your favorite"
                logger.info("The User {}  was removed the Event {} from his favorite", user.get_full_name(), event.name)
                removed = True
            else:
                message = "This Event was not found in your favorite"
                logger.warning("The Event {} was not found in the User {} favorite", event.name, user.get_full_name())
        else:
            message = "The Event was not found in this site"
            logger.error("The Event {} was not found", event_uuid)

        return event, removed, message

    
    @staticmethod
    def extract_event_data_from_form(request):
        data = None
        if request.method == 'POST':
            postdata = request.POST.copy()
            form = EventForm(postdata)
            if form.is_valid():
                data = form.cleaned_data
            else:
                logger.error("EventForm data is not valid")
                logger.error('EventForm Errors : %s\n', form.errors)
                logger.error('EventForm Non Field Errors : %s\n', form.non_field_errors)
        return data

    @staticmethod
    def event_update(pk=None, **event_data):
        '''
        This method update an Event and returns the Event that has been updated.
        None is returned when no Event could be found.
        '''
        event = None
        try:
            event = Event.objects.filter(pk=pk).update(**event_data)
        except Event.DoesNotExist as identifier:
            logger.error("Event Update Error : Could not find Event with id {}", pk)
        return event
    

    @staticmethod
    def cancel_events(**kwargs):
        '''
            return True when the Event has been canceled
                   False when the No Event could be found
        '''
        return 1 == Event.objects.filter(**kwargs).update(canceled= True, is_active=False, canceled_at=datetime.datetime.now())

    

    @staticmethod
    def create_event(**event_data):
        '''
            This method creates an Event with the **event_data and returns a tuple that contains an instance of the
            created Event an a boolean flag set to True
            A tuple containing the already existings Event is returned if the Event already existed and boolean flag
            set to False is returned.
        '''
        return Event.objects.get_or_create(**event_data)

    @staticmethod
    def create_category(category_name=None):
        category = None
        if category_name and not Category.objects.filter(name=category_name).exists():
            category = Category.objects.create(name=category_name, slug=slugify(category_name))
        return category

    @staticmethod
    def get_category_events(category_slug=None):
        events = None
        category = None
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                events = category.events.all()
            except Category.DoesNotExist as e:
                logger.error("No Category found with slug {}", category_slug)
            
        return events, category


    
    @staticmethod
    def event_summary(event_uuid=None):
        monitoring = None
        if event_uuid:
            try:
                event = Event.objects.get(event_uuid=event_uuid)
                participants = event.participants.count()
                likes = event.liked_by.count()
                monitoring = {
                    'participants' : participants,
                    'likes' : likes
                }
            except Event.DoesNotExists as e:
                logger.debug("Event with uuid {} not found", event_uuid)
        return monitoring


    @staticmethod
    def event_search(query=None):
        results = None
        if query:
            location = Q(where__icontains=query)
            name = Q(name__icontains=query)
            country = Q(country__icontains=query)
            city = Q(city__icontains=query)
            category = Q(category__name__icontains=query)
            address = Q(address__icontains=query)
            description = Q(description__icontains=query)
            results = Event.objects.filter(location | name | country | city | category | address | description )

        return results
    
    @classmethod
    def request_payment(cls, data=None):
        """
        send a payment request to the payment service

        Keyword arguments :
        url - the service url where the data are sent
        data - a dict representing the data to be sent.
        return None on error
        return the json response received from the payment service.
        """
        if not data:
            return None
        
        if not settings.PAY_REQUEST_URL or not settings.PAY_USERNAME or not settings.PAY_REQUEST_TOKEN:
            logger.warning('PAY:USER or PAY_REQUEST_TOKEN environment variable is not defined.')
            return None
        url = f"{settings.PAY_REQUEST_URL}/{settings.PAY_USERNAME}/{settings.PAY_REQUEST_TOKEN}/"
        headers={'Authorization': f"Token {settings.PAY_REQUEST_TOKEN}"}
        response = requests.post(url, data=data, headers=headers)
        if not response:
            logger.error(f"Error on requesting a payment to the url {url} : {response.status_code}")
            return None
        return response.json()['token']

    

