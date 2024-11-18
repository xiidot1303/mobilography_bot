from bot.bot import *
from app.services.price_service import *
from config import CHANNEL_JOIN_LINK


async def get_payment_provider(update: Update, context: CustomContext):
    _, provider = update.callback_query.data.split("--")
    # send invoice
    title = "Курс"
    description = "Секретная Технология из США (Отабек Одилов)"
    payload = "payload1303"
    currency = PAYMENT_PROVIDERS[provider]["currency"]
    price = await get_price_by_currency(currency)
    prices = [LabeledPrice("Подписка на канал", int(price * 100))]
    
    await context.bot.send_invoice(
        chat_id=context._user_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PAYMENT_PROVIDERS[provider]["token"],
        currency=currency,
        prices=prices,
        start_parameter="payment"
    )

    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context)

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    # Check the payload to make sure it matches what you sent
    if query.invoice_payload != "payload1303":
        # If the payload is invalid, answer with "False"
        await query.answer(ok=False, error_message="Something went wrong with the payment.")
    else:
        # If the payload is valid, answer with "True"
        await query.answer(ok=True)


async def successful_payment(update: Update, context: CustomContext) -> None:
    # give access to join channel
    bot_user: Bot_user = await get_object_by_update(update)
    bot_user.has_access_to_channel = True
    await bot_user.asave()

    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text=context.words.join_channel,
            url=CHANNEL_JOIN_LINK
        )
    ]])
    await update.message.reply_text(context.words.successful_payment, reply_markup=markup)

