from django.contrib.sitemaps import Sitemap
from .models import Landuse, Update


class LanduseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    limit = 1000
    protocol = 'https'

    def items(self):
        return Landuse.objects.filter(
            revision=Update.get_latest_update()
        ).all()

    def lastmod(self, obj: Landuse):
        return obj.revision.created_at
