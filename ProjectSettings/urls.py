from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from apps.article.models import Article
from django.urls import reverse

info_dict = {
    'queryset': Article.objects.filter(status='published'),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.article.urls', namespace='articles')),
    path('user/', include('apps.users.urls', namespace='users')),
    path('cases/', include('apps.cases.urls', namespace='cases')),
    path('captcha', include('captcha.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('robots.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': {'article': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
