from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm 
from .models import Bio, User, Service, Realisation

def home(request):
    try:
        bio = Bio.objects.latest('date_modification')
    except Bio.DoesNotExist:
        bio = None

    services = Service.objects.order_by('position')
    realisations = Realisation.objects.order_by('position')  # Fetch all realizations

    return render(request, 'home.html', {'bio': bio, 'services':services, 'realisations': realisations})

def biodet(request):
    try:
        bio = Bio.objects.latest('date_modification')
    except Bio.DoesNotExist:
        bio = None
    return render(request, 'biodet.html', {'bio': bio})

def inscription(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # Définit le mot de passe
            user.save()

            login(request, user)  # Connexion automatique après inscription
            return redirect('home')  # Redirige vers la page d'accueil ou une autre page
    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'inscription.html', {'user_form': user_form})