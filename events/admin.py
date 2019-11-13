from django.contrib import admin
from events.models import Event, Category
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    model = Event




admin.site.register(Category)
admin.site.register(Event)
