from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm 
from .models import Bio, User, Service, Realisation
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm

def home(request):
    """
    Page d'accueil pour les utilisateurs non connectés.
    Contient des liens d'inscription ou de connexion.
    """
    if request.user.is_authenticated:
        return redirect('home2')  # Redirige les utilisateurs connectés vers la page d'accueil des authentifiés

    try:
        bio = Bio.objects.latest('date_modification')
    except Bio.DoesNotExist:
        bio = None

    services = Service.objects.order_by('position')
    realisations = Realisation.objects.order_by('position')

    return render(request, 'home.html', {'bio': bio, 'services': services, 'realisations': realisations})

def home2(request):
    """
    Page d'accueil pour les utilisateurs connectés.
    Ne contient pas de liens d'inscription ou de connexion.
    """
    if not request.user.is_authenticated:
        return redirect('home')  # Si l'utilisateur n'est pas connecté, redirige vers l'accueil non connecté

    try:
        bio = Bio.objects.latest('date_modification')
    except Bio.DoesNotExist:
        bio = None

    services = Service.objects.order_by('position')
    realisations = Realisation.objects.order_by('position')

    return render(request, 'home2.html', {'bio': bio, 'services': services, 'realisations': realisations})

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
            return redirect('home2')  # Redirige vers la page d'accueil ou une autre page
    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'inscription.html', {'user_form': user_form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'connexion.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home2')  # Redirection après connexion réussie

    def get_success_url(self):
        return self.success_url
    
def connexion_view(request):
    context = {'form': LoginForm()}  # Assurez-vous que LoginForm est défini
    return render(request, 'my_app/connexion.html', context)
