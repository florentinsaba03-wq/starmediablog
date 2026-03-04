from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Comment
from .forms import CommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Like
from django.contrib.auth.models import User
from django.http import FileResponse
from .models import Guide
from .forms import SubscriberForm
from django.db.models import F
from django.db import IntegrityError




def home(request):

    # HERO ARTICLE (dernier article sport par exemple)
    hero = Article.objects.filter(
        status='published',
        category__slug='sport'
    ).order_by('-created_at').first()

    # ARTICLES SECONDAIRES
    secondary = Article.objects.filter(
        status='published',
        category__slug='sport'
    ).order_by('-created_at')[1:5]

    # TRENDING ARTICLES
    trending = Article.objects.filter(
        status='published',
        category__slug__in=['sport', 'musique', 'sociopolitique', 'divers']
    ).order_by('-views')[:5]

    # ARTICLES PAR CATÉGORIE
    sport_articles = Article.objects.filter(
        status='published',
        category__slug='sport'
    ).order_by('-created_at')[:5]

    musique_articles = Article.objects.filter(
        status='published',
        category__slug='musique'
    ).order_by('-created_at')[:5]

    sociopolitique_articles = Article.objects.filter(
        status='published',
        category__slug='sociopolitique'
    ).order_by('-created_at')[:5]

    divers_articles = Article.objects.filter(
        status='published',
        category__slug='divers'
    ).order_by('-created_at')[:5]

    context = {
        'hero': hero,
        'secondary': secondary,
        'trending': trending,
        'sport_articles': sport_articles,
        'musique_articles': musique_articles,
        'sociopolitique_articles': sociopolitique_articles,
        'divers_articles': divers_articles,
    }

    return render(request, 'home.html', context)



def article_detail(request, slug):

    article = get_object_or_404(Article, slug=slug,status='published')

    article.views += 1
    article.save()
    comments = article.comments.filter(active=True).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()
    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'article_detail.html', context)


def category_articles(request, slug):

    category = get_object_or_404(Category, slug=slug)

    articles_list = Article.objects.filter(
        category=category,
        status='published'
    ).order_by('-created_at')

    paginator = Paginator(articles_list, 6)

    page_number = request.GET.get('page')

    articles = paginator.get_page(page_number)

    context = {
        'category': category,
        'articles': articles
    }

    return render(request, 'category_articles.html', context)


from django.http import JsonResponse

@login_required
def like_article(request, slug):

    article = get_object_or_404(Article, slug=slug)

    like, created = Like.objects.get_or_create(
        article=article,
        user=request.user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'likes': article.likes.count(),
        'liked': liked
    })

def author_profile(request, username):

    author = get_object_or_404(User, username=username)

    articles = Article.objects.filter(
        author=author,
        status="published"
    )

    return render(request, "author_profile.html", {
        "author": author,
        "articles": articles
    })

@login_required
def dashboard(request):

    articles = Article.objects.filter(
        author=request.user
    )

    return render(request, "dashboard.html", {
        "articles": articles
    })

def capture_email(request, slug):
    guide = get_object_or_404(Guide, slug=slug)

    if request.method == "POST":
        form = SubscriberForm(request.POST)

        if form.is_valid():
            try:
                subscriber = form.save(commit=False)
                subscriber.guide = guide
                subscriber.save()
            except IntegrityError:
                # L'email existe déjà pour ce guide
                pass

            request.session[f'guide_access_{guide.id}'] = True
            return redirect('download_guide', slug=guide.slug)
    else:
        form = SubscriberForm()

    return render(request, 'capture.html', {
        'form': form,
        'guide': guide
    })


def download_guide(request, slug):
    guide = get_object_or_404(Guide, slug=slug)

    # 🔒 Vérifie si l'utilisateur a accès après capture email
    if not request.session.get(f'guide_access_{guide.id}'):
        return redirect('capture', slug=guide.slug)

    # 📊 Incrémentation atomique du compteur
    Guide.objects.filter(id=guide.id).update(
        downloads_count=F('downloads_count') + 1
    )

    # 📥 Téléchargement sécurisé du fichier
    return FileResponse(
        guide.pdf.open('rb'),
        as_attachment=True
    )
