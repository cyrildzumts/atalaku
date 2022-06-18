from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
# Create your models here.

PR_ACTIVE           = 'Active'
PR_CANCELED         = 'Canceled'
PR_CLEARED          = 'Cleared'
PR_ACCEPTED         = 'Accepted'
PR_CREATED          = 'Created'
PR_COMPLETED        = 'Completed'
PR_DECLINED         = 'Declined'
PR_EXPIRED          = 'Expired'
PR_FAILED           = 'Failed'
PR_PAID             = 'Paid'
PR_PROCESSED        = 'Processed'
PR_PENDING          = 'Pending'
PR_REFUSED          = 'Refused'
PR_REVERSED         = 'Reversed'

PR_STATUS = [
    PR_ACCEPTED,PR_ACTIVE, PR_CANCELED, PR_CLEARED,
    PR_COMPLETED, PR_CREATED, PR_DECLINED, PR_EXPIRED,
    PR_FAILED, PR_PAID, PR_PENDING, PR_PROCESSED, 
    PR_REFUSED, PR_REVERSED
]


def event_file_path(instance, filename):
    file_ext = filename.split(".")[-1]
    name = instance.name + "." + file_ext
    return "events/event_{0}_{1}".format(instance.user.id, name)

class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField()
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category_uuid = models.UUIDField(default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse("events:category-detail", kwargs={"pk": self.pk})
    
    def get_dashboard_url(self):
        return reverse("dashboard:category-detail", kwargs={"category_uuid": self.category_uuid})

    def get_dashboard_update_url(self):
        return reverse("dashboard:category-update", kwargs={"category_uuid": self.category_uuid})

    def __str__(self):
        return self.name

class Event(models.Model):
    participants = models.ManyToManyField(User,related_name='registered_events', blank=True)
    liked_by = models.ManyToManyField(User, related_name='favorite_events', blank=True)
    published_by = models.ForeignKey(User, related_name='published_events', blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='events', blank=True, null=True)
    
    when = models.DateTimeField(null=False, blank=False)
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
    #created_by = models.ForeignKey(User, related_name='created_events', blank=True, null=True, on_delete=models.SET_NULL)
    canceled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_uuid = models.UUIDField(default=uuid.uuid4)
    slug = models.SlugField()
    
    def get_absolute_url(self):
        return reverse("events:event-detail", kwargs={"event_uuid": self.event_uuid})
    
    def get_dashboard_url(self):
        return reverse("dashboard:event-detail", kwargs={"event_uuid": self.event_uuid})

    def get_dashboard_update_url(self):
        return reverse("dashboard:event-update", kwargs={"event_uuid": self.event_uuid})
    
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
    ticket_uuid = models.UUIDField(default=uuid.uuid4)
    ticket_code = models.CharField(max_length=32, blank=True, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, related_name="buyed_tickets", blank=True, null=True, on_delete=models.SET_NULL)
    cancel_delai = models.IntegerField(default=0, blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        permissions = (
            ('api_view_event_ticket', 'Can View event ticket through rest api'),
            ('api_edit_event_ticket', 'Can change event ticket through rest api'),
            ('api_add_event_ticket', 'Can add event ticket through rest api'),
            ('api_delete_event_ticket', 'Can delete event ticket through rest api'),
        )

    def __str__(self):
        return self.ticket_code 
    

    def get_absolute_url(self):
        return reverse("events:ticket-detail", kwargs={"ticket_uuid": self.ticket_uuid})
    
    def get_dashboard_url(self):
        return reverse("dashboard:ticket-detail", kwargs={"ticket_uuid": self.ticket_uuid})




class PaymentRequest(models.Model):
    token = models.CharField(max_length=32, blank=True, null=True)
    verification_code = models.TextField(max_length=80, blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE ,blank=False )
    amount = models.DecimalField(max_digits=10,decimal_places=2, blank=False, null=False)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    tva = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    commission = models.DecimalField(max_digits=5,decimal_places=4, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default=PR_CREATED, blank=False, null=False)
    product_name = models.CharField(max_length=255 ,blank=False, null=False)
    customer_name = models.CharField(max_length=255 ,blank=False, null=False)
    description = models.CharField(max_length=255 ,blank=False, null=False)

