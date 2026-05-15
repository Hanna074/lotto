from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('manager/', include('manager.urls')),
    path('', include('lotto.urls')),
]
