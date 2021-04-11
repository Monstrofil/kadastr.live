from django.contrib.sitemaps import Sitemap
from .models import Landuse


class LanduseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    limit = 1000
    protocol = 'https'

    def items(self):
        return Landuse.objects.order_by('cadnum').all()

    def lastmod(self, obj):
        return None
