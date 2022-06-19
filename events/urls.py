from django.conf.urls import url, include
from django.urls import path, reverse_lazy

from events import views

app_name = 'events'


urlpatterns = [
    path('', views.event_home, name='event-home'),
    path('events/<slug:category_slug>/', views.event_category_events, name='category-detail'),
    path('event-home/', views.event_home, name='event-home'),
    path('event-list/', views.events, name='events'),
    path('event-create/', views.event_create, name='event-create'),
    path('event-category-create/', views.create_event_category, name='event-category-create'),
    path('event-detail/<uuid:event_uuid>/', views.event_detail, name='event-detail'),
    path('events/<slug:category_slug>/<slug:slug>/', views.event_detail_slug, name='event-detail'),
    path('event-delete/<uuid:event_uuid>/', views.event_detail, name='event-delete'),
    path('event-update/<uuid:event_uuid>/', views.event_update, name='event-update'),
    path('event-cancel/<uuid:event_uuid>/', views.event_cancel, name='event-cancel'),
    path('event-buy-ticket/<uuid:event_uuid>/', views.event_buy_ticket, name='event-buy-ticket'),
    path('search/', views.event_search, name='search'),
    path('event-add-participant/<uuid:event_uuid>/', views.event_add_participant, name='event-add-participant'),
    path('event-remove-participant/<uuid:event_uuid>/', views.event_remove_participant, name='event-remove-participant'),
    path('event-like/<uuid:event_uuid>/', views.event_like, name='event-like'),
    path('event-unlike/<uuid:event_uuid>/', views.event_unlike, name='event-unlike'),
]