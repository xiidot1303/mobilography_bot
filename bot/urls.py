from django.urls import path, re_path
from config import BOT_API_TOKEN
from django.conf import settings
from django.conf.urls.static import static
from config import DEBUG
from bot.views import botwebhook, web_app

urlpatterns = [
    path(BOT_API_TOKEN, botwebhook.BotWebhookView.as_view()),
    path("view-video", web_app.view_video),
    path("personal-info-form", web_app.PersonalInfoForm.as_view()),
]

if DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)