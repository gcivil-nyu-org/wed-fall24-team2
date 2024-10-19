from django.shortcuts import render
from django.forms.models import model_to_dict
import os, json
from chatroom.models import Chatroom

def homepage(request):
    return render(request, 'homepage.html', {
        'mapbox_access_token': os.environ.get('MAPBOX_ACCESS_TOKEN'),
        'chatrooms': json.dumps([model_to_dict(chatroom) for chatroom in Chatroom.objects.all()])
    })
