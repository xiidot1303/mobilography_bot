from bot import *
from bot.utils.keyboards import *


async def send_payment_providers(application: Application, user_id):
    text = Strings(user_id=user_id).choose_payment_method
    markup = payment_providers_keyboard
    await application.update_queue.put(NewsletterUpdate(
        user_id=user_id,
        text=text,
        reply_markup=markup
    ))
