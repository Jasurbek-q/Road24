from django.contrib import admin
from django.urls import path
from .views import bot_webhook
urlpatterns = [
    path('webhook/', bot_webhook, name='bot_webhook'),
    # path('stats/', button_stats, name='button_stats'),
    path('admin/', admin.site.urls),  # Django admin paneli
]
