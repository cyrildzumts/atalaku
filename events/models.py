from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
# Create your models here.

def event_file_path(instance, filename):
    file_ext = filename.split(".")[-1]
    name = instance.name + "." + file_ext
    return "events/event_{0}_{1}".format(instance.user.id, name)

class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField()
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("events:category-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name

class Event(models.Model):
    participants = models.ManyToManyField(User,related_name='registered_events', blank=True)
    liked_by = models.ManyToManyField(User, related_name='favorite_events', blank=True)
    published_by = models.ForeignKey(User, related_name='published_events', blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='events', blank=True, null=True)
    
    when = models.DateField(null=False, blank=False)
    where = models.CharField(max_length=64,null=False, blank=False)
    start = models.DateField(null=False, blank=False)
    end = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=event_file_path,null=True, blank=True)
    country = models.CharField(max_length=64,null=False, blank=False)
    
    city = models.CharField(max_length=64,null=False, blank=False)
    address = models.CharField(max_length=80,null=False, blank=False)
    name = models.CharField(max_length=64,null=False, blank=False)
    description = models.CharField(max_length=512,null=False, blank=False)
    entree_fee = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=10)
    
    organised_by = models.CharField(max_length=128,null=False, blank=False)
    views_count = models.IntegerField(default=0)
    free = models.BooleanField()
    canceled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    taking_part = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_uuid = models.UUIDField(default=uuid.uuid4())
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("events:event-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name
    

    class Meta:
        permissions = (
            ('api_view_event', 'Can View event through rest api'),
            ('api_edit_event', 'Can change event through rest api'),
            ('api_add_event', 'Can add event through rest api'),
            ('api_delete_event', 'Can delete event through rest api'),
        )



class EventTicket(models.Model):
    event = models.ForeignKey(Event, related_name="tickets", blank=True, null=True, on_delete=models.SET_NULL)
    ticket_uuid = models.UUIDField(default=uuid.uuid4())
    ticket_code = models.CharField(max_length=32, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, related_name="buyed_tickets", blank=True, null=True, on_delete=models.SET_NULL)
    cancel_delai = models.IntegerField(default=0)
    canceled_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        permissions = (
            ('api_view_event_ticket', 'Can View event ticket through rest api'),
            ('api_edit_event_ticket', 'Can change event ticket through rest api'),
            ('api_add_event_ticket', 'Can add event ticket through rest api'),
            ('api_delete_event_ticket', 'Can delete event ticket through rest api'),
        )