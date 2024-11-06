from django.shortcuts import render


def chatroom(request, chatroom_name):
    context = {
        "chatroom_name": chatroom_name,
    }
    return render(request, "chatroom.html", context)
