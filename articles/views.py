from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Comment, Like, Guide
from .forms import CommentForm, SubscriberForm
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.db import IntegrityError


def home(request):

    hero = Article.objects.filter(
        status='published'
    ).order_by('-created_at').first()

    secondary = Article.objects.filter(
        status='published'
    ).exclude(
        pk=hero.pk if hero else None
    ).order_by('-created_at')[:4]

    already_shown = list(
        secondary.values_list('pk', flat=True)
    )
    if hero:
        already_shown.append(hero.pk)

    sport_articles = Article.objects.filter(
        status='published',
        category__slug='sport'
    ).exclude(pk__in=already_shown).order_by('-created_at')[:4]

    musique_articles = Article.objects.filter(
        status='published',
        category__slug='musique'
    ).exclude(pk__in=already_shown).order_by('-created_at')[:4]

    sociopolitique_articles = Article.objects.filter(
        status='published',
        category__slug='sociopolitique'
    ).exclude(pk__in=already_shown).order_by('-created_at')[:4]

    divers_articles = Article.objects.filter(
        status='published',
        category__slug='divers'
    ).exclude(pk__in=already_shown).order_by('-created_at')[:4]

    all_section_ids = already_shown + list(
        sport_articles.values_list('pk', flat=True)
    ) + list(
        musique_articles.values_list('pk', flat=True)
    ) + list(
        sociopolitique_articles.values_list('pk', flat=True)
    ) + list(
        divers_articles.values_list('pk', flat=True)
    )

    a_la_une = Article.objects.filter(
        status='published'
    ).exclude(
        pk__in=all_section_ids
    ).order_by('-views')[:5]

    if a_la_une.count() < 3:
        a_la_une = Article.objects.filter(
            status='published'
        ).order_by('-views')[:5]

    categories = Category.objects.all()

    context = {
        'hero': hero,
        'secondary': secondary,
        'a_la_une': a_la_une,
        'sport_articles': sport_articles,
        'musique_articles': musique_articles,
        'sociopolitique_articles': sociopolitique_articles,
        'divers_articles': divers_articles,
        'categories': categories,
    }

    return render(request, 'home.html', context)


def article_detail(request, slug):

    article = get_object_or_404(
        Article, slug=slug, status='published'
    )

    Article.objects.filter(pk=article.pk).update(
        views=F('views') + 1
    )
    article.refresh_from_db()

    similaires = Article.objects.filter(
        status='published',
        category=article.category
    ).exclude(pk=article.pk).order_by('-created_at')[:3]

    suivant = Article.objects.filter(
        created_at__gt=article.created_at,
        status='published'
    ).order_by('created_at').first()

    precedent = Article.objects.filter(
        created_at__lt=article.created_at,
        status='published'
    ).order_by('-created_at').first()

    mots = len(article.content.split())
    temps_lecture = max(1, mots // 200)

    comments = article.comments.filter(
        active=True
    ).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'similaires': similaires,
        'suivant': suivant,
        'precedent': precedent,
        'temps_lecture': temps_lecture,
    }

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


def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        name = request.POST.get("name", "").strip()

        if not email:
            return JsonResponse({
                "success": False,
                "message": "Email obligatoire."
            })

        try:
            from .models import Subscriber
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={"name": name}
            )
            if created:
                return JsonResponse({
                    "success": True,
                    "message": "Abonnement réussi ! Bienvenue 🎉"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Cet email est déjà inscrit. ✅"
                })
        except Exception:
            return JsonResponse({
                "success": False,
                "message": "Erreur lors de l'inscription."
            })

    return JsonResponse({
        "success": False,
        "message": "Méthode non autorisée."
    })


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
    ).order_by('-created_at')

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

    if not request.session.get(f'guide_access_{guide.id}'):
        return redirect('capture', slug=guide.slug)

    Guide.objects.filter(id=guide.id).update(
        downloads_count=F('downloads_count') + 1
    )

    return FileResponse(
        guide.pdf.open('rb'),
        as_attachment=True
    )


def google_verification(request):
    return HttpResponse(
        "google-site-verification: google5800450418fec533.html"
    )