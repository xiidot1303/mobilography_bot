from bot.control.handlers import successfully_payment_handler
from bot.control.updater import application, CustomContext
from telegram import Update, Message, Chat, User, SuccessfulPayment
from telegram.ext import Updater


async def send_manual_successful_payment(user_id):
    user = User(id=user_id, first_name=".", is_bot=False)

    chat = Chat(id=user_id, type="private")

    successful_payment = SuccessfulPayment(
        currency="USD",
        total_amount=1000,
        invoice_payload="invoice_payload",
        telegram_payment_charge_id="payment_charge_id",
        provider_payment_charge_id="provider_charge_id"
    )

    message = Message(
        message_id=1,
        date=None,
        chat=chat,
        from_user=user,
        successful_payment=successful_payment
    )

    update = Update(update_id=1, message=message)
    await application.update_queue.put(update)
    # await successfully_payment_handler.callback(update, CustomContext(application))
