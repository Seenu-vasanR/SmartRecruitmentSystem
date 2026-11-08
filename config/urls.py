from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_accounts import views as user_views

urlpatterns = [
    path('', user_views.home_page, name='home'),

    path('admin/', admin.site.urls),

    path('accounts/', include('user_accounts.urls')),

    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )