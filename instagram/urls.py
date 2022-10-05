from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .settings import MEDIA_URL, MEDIA_ROOT
from content.views import UploadFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('', include('content.urls')),
    path('', include('user.urls')),
    path('content/upload', UploadFeed.as_view()),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
