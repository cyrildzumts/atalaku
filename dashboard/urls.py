from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('home/', views.dashboard_home, name='home'),
    path('category-create/', views.category_create, name='category-create'),
    path('categories/', views.categories, name='categories'),
    path('categories/<uuid:category_uuid>/', views.category_detail, name='category-detail'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/update/<uuid:category_uuid>/', views.category_update, name='category-update'),
    path('events/', views.events, name='events'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/<category_slug>/', views.event_category_events, name='category-events'),
    path('event-detail/<uuid:event_uuid>/', views.event_detail, name='event-detail'),
    path('events/delete/<uuid:event_uuid>/', views.event_detail, name='event-delete'),
    path('events/update/<uuid:event_uuid>/', views.event_update, name='event-update'),
    path('events/cancel/<uuid:event_uuid>/', views.event_cancel, name='event-cancel'),
    path('event-search/', views.event_search, name='event-search'),
    path('event-search/<query>/', views.event_search, name='event-search'),
    path('event-add-participant/<uuid:event_uuid>/', views.event_add_participant, name='event-add-participant'),
    path('event-remove-participant/<uuid:event_uuid>/', views.event_remove_participant, name='event-remove-participant'),
    path('generate-token/', views.generate_token, name='generate-token'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:pk>/', views.group_detail, name='group-detail'),
    path('groups/create/', views.group_create, name='group-create'),
    path('groups/delete/<int:pk>/', views.group_delete, name='group-delete'),
    path('groups/update/<int:pk>/', views.group_update, name='group-update'),
    path('tickets/', views.event_tickets, name='tickets'),
    path('tickets/<uuid:ticket_uuid>', views.ticket_detail, name='ticket-detail'),
    path('tokens/', views.tokens, name='tokens'),
    path('users/', views.users, name='users'),
    path('userss/<int:pk>/', views.user_detail, name='user-detail'),
]