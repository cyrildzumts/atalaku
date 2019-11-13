from django.conf.urls import url, include
from django.urls import path, reverse_lazy

from events import views

app_name = 'events'


urlpatterns = [
    path('', views.event_home, name='event-home'),
    path('events/<category_slug>/', views.event_category_events, name='category-events'),
    path('event-home/', views.event_home, name='event-home'),
    path('event-list/', views.events, name='events'),
    path('event-create/', views.event_create, name='event-create'),
    path('event-category-create/', views.create_event_category, name='event-category-create'),
    path('event-detail/<event_uuid>/', views.event_detail, name='event-detail'),
    path('event-delete/<event_uuid>/', views.event_detail, name='event-delete'),
    path('event-update/<event_uuid>/', views.event_update, name='event-update'),
    path('event-cancel/<event_uuid>/', views.event_cancel, name='event-cancel'),
    path('event-buy-ticket/<event_uuid>/', views.event_buy_ticket, name='event-buy-ticket'),
    path('event-search/', views.event_search, name='event-search'),
    path('event-search/<query>/', views.event_search, name='event-search'),
    path('event-add-participant/<event_uuid>/', views.event_add_participant, name='event-add-participant'),
    path('event-remove-participant/<event_uuid>/', views.event_remove_participant, name='event-remove-participant'),
    path('event-like/<event_uuid>/', views.event_like, name='event-like'),
    path('event-unlike/<event_uuid>/', views.event_unlike, name='event-unlike'),
]