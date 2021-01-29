from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = []

apipatterns = []

urlpatterns += apipatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIAROOT)
    urlpatterns += [path('admin/', admin.site.urls)]
else:
    urlpatterns += [path('management/', admin.site.urls)]