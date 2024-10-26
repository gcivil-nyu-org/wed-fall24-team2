from django.shortcuts import render


def chatroom(request):
    return render(request, "chatroom.html")
