from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # ══ AUTHENTIFICATION ══
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='home'   # ✅ redirige vers home, pas login
        ),
        name='logout'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    # ══ PROFIL UTILISATEUR CONNECTÉ ══
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # ✅ author_profile SUPPRIMÉ ICI
    # → Il est déjà déclaré dans articles/urls.py
    # → Garder les deux crée un conflit de nom silencieux

]