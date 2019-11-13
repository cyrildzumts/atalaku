from django.urls import resolve
from django.test import TestCase
import unittest
from events import views

# Create your tests here.

class EventViewsUrlsTest(TestCase):

    def test_event_home_resolve(self):
        found = resolve('/events/')
        self.assertEqual(found.func, views.event_home)
        found = resolve('/events/event-home/')
        self.assertEqual(found.func, views.event_home)
    

    def test_event_list_resolve(self):
        found = resolve('/events/event-list/')
        self.assertEqual(found.func, views.events)

    
    def test_event_create_resolve(self):
        found = resolve('/events/event-create/')
        self.assertEqual(found.func, views.event_create)

    def test_event_category_create_resolve(self):
        found = resolve('/events/event-category-create/')
        self.assertEqual(found.func, views.create_event_category)


    def test_event_detail_resolve(self):
        found = resolve('/events/event-detail/145752/')
        self.assertEqual(found.func, views.event_detail)
    


    def test_event_update_resolve(self):
        found = resolve('/events/event-update/145752/')
        self.assertEqual(found.func, views.event_update)
    

    def test_event_cancel_resolve(self):
        found = resolve('/events/event-cancel/145752/')
        self.assertEqual(found.func, views.event_cancel)

    
    def test_event_like_resolve(self):
        found = resolve('/events/event-like/145752/')
        self.assertEqual(found.func, views.event_like)


    def test_event_unlike_resolve(self):
        found = resolve('/events/event-unlike/145752/')
        self.assertEqual(found.func, views.event_unlike)

    
    def test_event_add_participant_resolve(self):
        found = resolve('/events/event-add-participant/145752/')
        self.assertEqual(found.func, views.event_add_participant)

    
    def test_event_remove_participant_resolve(self):
        found = resolve('/events/event-remove-participant/145752/')
        self.assertEqual(found.func, views.event_remove_participant)
    

    def test_event_search_resolve(self):
        found = resolve('/events/event-search/')
        self.assertEqual(found.func, views.event_search)
        found = resolve('/events/event-search/1458789/')
        self.assertEqual(found.func, views.event_search)
    