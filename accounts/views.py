from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from articles.models import Article


# ══ REGISTER ══
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# ══ PROFIL UTILISATEUR CONNECTÉ ══
@login_required
def profile(request):
    articles = Article.objects.filter(
        author=request.user
    ).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'articles': articles
    })