from bot.models import Message, Bot_user, Alert
from bot.control.updater import application
from bot import NewsletterUpdate, InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
import asyncio
from app.utils import datetime_now


async def send_message():
    async for message in Message.objects.filter(is_sent=False):
        # save message as sent
        message.is_sent = True
        await message.asave()
        # get users
        users = Bot_user.objects.all().values_list('user_id', flat=True)
        async for user_id in users:
            await application.update_queue.put(NewsletterUpdate(
                user_id=int(user_id),
                text=message.text,
                photo=f"{settings.MEDIA_URL}/{message.photo.name}" if message.photo else None,
                video=f"{settings.MEDIA_URL}/{message.video.name}" if message.video else None,
                document=f"{settings.MEDIA_URL}/{message.file.name}" if message.file else None
            ))


async def send_alerts():
    async for alert in Alert.objects.filter(datetime__lte = await datetime_now()):
        if await alert.is_active:
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=alert.button_text,
                    url=alert.url
                )
            ]])
            await application.update_queue.put(NewsletterUpdate(
                user_id=alert.bot_user.user_id,
                text=alert.text,
                reply_markup=markup
            ))
        await alert.adelete()