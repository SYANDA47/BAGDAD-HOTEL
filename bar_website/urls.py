from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bar_app.urls')),
    path('accommodation/', include('accommodation.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),  # Added orders URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
