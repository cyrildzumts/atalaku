from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('home/', views.dashboard_home, name='home'),
    path('events/', views.events, name='events'),
    path('events/event-create/', views.event_create, name='event-create'),
    path('events/<category_slug>/', views.event_category_events, name='category-events'),
    path('event-category-create/', views.create_event_category, name='event-category-create'),
    path('event-detail/<uuid:event_uuid>/', views.event_detail, name='event-detail'),
    path('event-delete/<uuid:event_uuid>/', views.event_detail, name='event-delete'),
    path('event-update/<uuid:event_uuid>/', views.event_update, name='event-update'),
    path('event-cancel/<uuid:event_uuid>/', views.event_cancel, name='event-cancel'),
    path('event-search/', views.event_search, name='event-search'),
    path('event-search/<query>/', views.event_search, name='event-search'),
    path('event-add-participant/<uuid:event_uuid>/', views.event_add_participant, name='event-add-participant'),
    path('event-remove-participant/<uuid:event_uuid>/', views.event_remove_participant, name='event-remove-participant'),
    path('tickets/', views.event_tickets, name='tickets'),
    path('tickets/<uuid:ticket_uuid>', views.ticket_detail, name='ticket-detail'),
]