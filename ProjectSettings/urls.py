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

info_dict = {
    'queryset': Article.objects.filter(status='published'),
}

admin.site.site_header = 'Injection 后台'
admin.site.site_title = 'Injection 后台'


def dandh811(request):
    return HttpResponse(1)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.article.urls', namespace='articles')),
    path('user/', include('apps.users.urls', namespace='users')),
    path('cases/', include('apps.cases.urls', namespace='cases')),
    path('tools/', include('apps.tools.urls', namespace='tools')),
    path('mdeditor/', include('mdeditor.urls')),
    path('captcha', include('captcha.urls')),
    path('task/', include('apps.tasks.urls', namespace='task')),
    path('toolkit/', include('apps.toolkit.urls', namespace='toolkit')),
    path('sectest/', include('apps.sectest.urls', namespace='sectest')),
    path('financial/', include('apps.financial.urls', namespace='financial')),

    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # path('robots.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': {'article': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)