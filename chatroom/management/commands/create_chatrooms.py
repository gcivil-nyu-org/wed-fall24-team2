from django.core.management.base import BaseCommand
from chatroom.models import Chatroom

class Command(BaseCommand):
    help = 'Create chatrooms'

    def handle(self, *args, **kwargs):
        chatrooms = [
            {
                'name': 'Manhattan',
                'address': '1 Centre Street',
                'city': 'New York',
                'state': 'NY',
                'country': 'USA',
                'zipcode': '10007',
                'description': 'The heart of New York City with iconic skyscrapers and attractions',
                'latitude': 40.7831,
                'longitude': -73.9712,
            },
            {
                'name': 'Brooklyn',
                'address': '209 Joralemon Street',
                'city': 'Brooklyn',
                'state': 'NY',
                'country': 'USA',
                'zipcode': '11201',
                'description': 'A diverse borough known for its artistic communities and brownstone buildings',
                'latitude': 40.6782,
                'longitude': -73.9442,
            },
            {
                'name': 'Queens',
                'address': '120-55 Queens Blvd',
                'city': 'Queens',
                'state': 'NY',
                'country': 'USA',
                'zipcode': '11424',
                'description': 'The largest borough by area featuring diverse communities and cultures',
                'latitude': 40.7282,
                'longitude': -73.7949,
            },
            {
                'name': 'The Bronx',
                'address': '851 Grand Concourse',
                'city': 'Bronx',
                'state': 'NY',
                'country': 'USA',
                'zipcode': '10451',
                'description': 'Home to the Yankee Stadium and the Bronx Zoo',
                'latitude': 40.837,
                'longitude': -73.8654,
            },
            {
                'name': 'Staten Island',
                'address': '10 Richmond Terrace',
                'city': 'Staten Island',
                'state': 'NY',
                'country': 'USA',
                'zipcode': '10301',
                'description': 'The most suburban of NYC\'s boroughs with ferry access to Manhattan',
                'latitude': 40.5795,
                'longitude': -74.1502,
            },
        ]

        for chatroom_data in chatrooms:
            if not Chatroom.objects.filter(name=chatroom_data['name']).exists():
                Chatroom.objects.create(**chatroom_data)
        print('Chatrooms has been created')


