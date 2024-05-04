import json
from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event, EventRegistration
from .models import CustomUser

class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user()
        self.event = self.create_event()
        self.event_registration = self.create_event_registration()

    def create_user(self):
        return CustomUser.objects.create_user(username='testuser', password='testpassword')

    def create_event(self):
        return Event.objects.create(
            title='Event Title',
            description='Event Description',
            date='2024-05-03T12:00:00Z',
            location='Event Location',
            organizer=self.user
        )

    def create_event_registration(self):
        return EventRegistration.objects.create(
            user=self.user,
            event=self.event
        )

    def test_event_list(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_detail(self):
        response = self.client.get(reverse('event-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Event Title')

    def test_event_create(self):
        data = {
            'title': 'New Event Title',
            'description': 'New Event Description',
            'date': '2024-05-04T12:00:00Z',
            'location': 'New Event Location',
            'organizer': self.user.pk
        }
        response = self.client.post(reverse('event-create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 2)

    def test_event_update(self):
        data = {
            'title': 'Updated Event Title',
            'description': 'Updated Event Description',
            'date': '2024-05-05T12:00:00Z',
            'location': 'Updated Event Location',
            'organizer': self.user.pk
        }
        response = self.client.put(reverse('event-update', kwargs={'pk': self.event.pk}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event Title')

    def test_event_delete(self):
        response = self.client.delete(reverse('event-delete', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Event.objects.count(), 0)

    def test_event_filter_by_title(self):
        response = self.client.get(reverse('event-list'), data={'title': 'Event Title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_filter_by_description(self):
        response = self.client.get(reverse('event-list'), data={'description': 'Event Description'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_filter_by_location(self):
        response = self.client.get(reverse('event-list'), data={'location': 'Event Location'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_filter_by_date(self):
        response = self.client.get(reverse('event-list'), data={'date': '2024-05-03T12:00:00Z'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_filter_by_organizer(self):
        response = self.client.get(reverse('event-list'), data={'organizer': self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_filter_by_registration_date(self):
        response = self.client.get(reverse('event-list'), data={'registration_date': '2024-05-03T12:00:00Z'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_event_search(self):
        response = self.client.get(reverse('event-list'), data={'search': 'Event Title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
