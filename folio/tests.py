from django.test import TestCase
from django.urls import reverse
from .models import User

class UserModelTests(TestCase):

    def setUp(self):
        # Crée un utilisateur en utilisant l'email comme identifiant
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='securepassword',
            noms='Test User'
        )

    def test_user_creation(self):
        # Vérifie si l'utilisateur a été créé correctement
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('securepassword'))
        self.assertEqual(self.user.noms, 'Test User')

    
    def test_accueil1_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_accueil2_view(self):
        self.client.login(email='testuser@example.com', password='securepassword')  # Assurez-vous que vous avez un utilisateur test
        response = self.client.get(reverse('home2'))
        self.assertEqual(response.status_code, 200)

    def test_inscription_view(self):
        response = self.client.get(reverse('inscription'))
        self.assertEqual(response.status_code, 200)

    def test_connexion_view(self):
        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)

    def test_valid_user_creation(self):
        response = self.client.post(reverse('inscription'), {
            'email': 'testuser@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'noms': 'Test User',
        })
        self.assertEqual(response.status_code, 302)  # Redirection après inscription

    def test_invalid_user_creation(self):
        response = self.client.post(reverse('inscription'), {
            'email': 'testuser@example.com',
            'password1': 'securepassword',
            'password2': 'differentpassword',
            'noms': 'Test User',
        })
        self.assertEqual(response.status_code, 200)  # Formulaire de retour avec erreurs
        self.assertContains(response, 'Les mots de passe ne correspondent pas')

    def test_valid_login(self):
        self.client.post(reverse('inscription'), {
            'email': 'testuser@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'noms': 'Test User',
        })
        response = self.client.post(reverse('connexion'), {
            'email': 'testuser@example.com',
            'password': 'securepassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirection après connexion

    def test_invalid_login(self):
        response = self.client.post(reverse('connexion'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Formulaire de retour avec erreurs
        self.assertContains(response, 'Identifiants invalides')

