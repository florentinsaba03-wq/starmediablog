from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from articles.models import Article


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def profile(request, username):

    user = User.objects.get(username=username)

    articles = Article.objects.filter(
        author=user,
        status="published"
    )

    return render(request, "accounts/profile.html", {

        "profile_user": user,
        "articles": articles

    })