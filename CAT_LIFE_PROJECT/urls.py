from django.contrib import admin
from django.urls import path, include
from core.views import IndexView, ProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', IndexView.as_view(), name='index'),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('profile/', ProfileView.as_view(), name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)