from events.models import Event, Category, EventTicket, PaymentRequest
from django import forms
from django.utils import timezone

DECIMAL_PLACES = 2

class EventSearchForm(forms.Form):
    query = forms.CharField(max_length=32)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['when','start','end', 'where','category', 'country', 'city', 'address', 'name', 'description', 'entree_fee', 'free', 'organised_by']




class EventCancelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['canceled']



class TicketForm(forms.ModelForm):
    class Meta:
        model = EventTicket
        fields = ['event', 'price', 'buyer', 'ticket_code']

class PaymentRequestForm(forms.Form):
    
    class Meta:
        model = PaymentRequest
        fields = ['token', 'seller', 'amount', 'unit_price','quantity', 'tva', 'commission',
        'country', 'status', 'product_name', 'customer_name', 'description'
        ]
