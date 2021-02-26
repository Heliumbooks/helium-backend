from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = []

apipatterns = [
    path('api/v1/auth/', include('helium_backend.authentication.api_urls')),
    path('api/v1/libraries/', include('helium_backend.libraries.api_urls')),
    path('api/v1/orders/', include('helium_backend.orders.api_urls')),
    path('api/v1/stripe/', include('helium_backend.stripe.api_urls')),
]

urlpatterns = apipatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('admin/', admin.site.urls)]
else:
    urlpatterns += [path('management/', admin.site.urls)]