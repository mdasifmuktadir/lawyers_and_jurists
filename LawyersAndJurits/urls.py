from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Lawyers & Jurists"  # Replaces 'Django Administration' top bar banner
admin.site.site_title = "Lawyers & Jurists"          # Replaces 'Django site admin' in the browser tab title
admin.site.index_title = "Welcome to the Lawyers & Jurists Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('api/', include('visual.urls')),
    path('api/', include('interface.urls')),
    path('api/', include('main.urls')),
    path('auth/', include('auth.urls')),
    # path('', include('main.urls')),
]

# Serves uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

