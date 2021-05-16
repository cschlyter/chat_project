from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    return render(request, 'chat/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login_page')

        context = {'form': form}
        return render(request, 'chat/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

        context = {}
        return render(request, 'chat/login.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login')
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
