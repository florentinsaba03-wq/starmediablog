from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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


@login_required
def profile(request):

    user = request.user

    articles = Article.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,
        'articles': articles
    }

    return render(request, 'accounts/profile.html', context)


from django.contrib.auth.models import User

def author_profile(request, username):

    author = User.objects.get(username=username)

    articles = Article.objects.filter(
        author=author,
        status='published'
    ).order_by('-created_at')

    context = {
        'author': author,
        'articles': articles
    }

    return render(request, 'author_profile.html', context)