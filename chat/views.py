from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def register(request):
    context = {}
    return render(request, 'chat/register.html', context)


def login(request):
    context = {}
    return render(request, 'chat/login.html', context)


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
