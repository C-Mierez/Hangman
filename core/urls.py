from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: Landing Page
    # path('', )
    path('game/', include('game.urls')),
]
