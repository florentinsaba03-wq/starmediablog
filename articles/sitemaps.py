from django.contrib.sitemaps import Sitemap
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.9
    protocol = "https"  # ← Ajoute https

    def items(self):
        return Article.objects.filter(status="published").order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()  # ← Utilise ton get_absolute_url existant


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"/category/{obj.slug}/"


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return [
            '/',
            '/category/sport/',
            '/category/musique/',
            '/category/sociopolitique/',
            '/category/divers/',
        ]

    def location(self, item):
        return item