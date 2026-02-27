from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Comment
from .forms import CommentForm
from django.core.paginator import Paginator


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