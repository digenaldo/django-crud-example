from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('products.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)