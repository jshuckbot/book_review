from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.views import profile

# from reviewsapp.admin import admin_site

urlpatterns = [
    path("accounts/", include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path("accounts/profile/", profile, name='profile'),
    path("admin/", admin.site.urls),
    path("", include("reviewsapp.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
