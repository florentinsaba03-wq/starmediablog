"""
URL configuration for mediablog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from articles.sitemaps import ArticleSitemap, CategorySitemap, StaticSitemap

sitemaps = {
    'articles':   ArticleSitemap,
    'categories': CategorySitemap,
    'static':     StaticSitemap,
}

urlpatterns = [

    # ══ ADMIN ══
    path('admin/', admin.site.urls),

    # ══ APPS ══
    path('', include('articles.urls')),
    path('accounts/', include('accounts.urls')),

    # ══ CKEDITOR 5 ══
    path('django_ckeditor_5/', include('django_ckeditor_5.urls')),

    # ══ SEO ══
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        ),
        name='robots'
    ),

]

# Media files en développement uniquement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )