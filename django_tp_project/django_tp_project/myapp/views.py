from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature


def index(request):
    features = Feature.objects.all()
    context = {
        'name': 'Sara',
        'age': 30,
        'moroccan': True,
        'features': features,
    }
    return render(request, 'index.html', context)


def counter(request):
    text = request.POST.get('text', '') if request.method == 'POST' else request.GET.get('text', '')
    amount_of_words = len(text.split()) if text.strip() else 0
    return render(request, 'counter.html', {
        'amount': amount_of_words,
        'text': text,
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "L'email existe déjà.")
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.info(request, "Le nom d'utilisateur existe déjà.")
                return redirect('register')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')

        messages.info(request, 'Les mots de passe ne sont pas identiques.')
        return redirect('register')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        messages.info(request, 'Identifiants invalides.')
        return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
