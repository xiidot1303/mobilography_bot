from bot.bot import *
from app.services.price_service import *
from config import CHANNEL_JOIN_LINK
from app.services.payment_service import *
from payment.services.cryptocloud_service import *


async def get_payment_provider(update: Update, context: CustomContext):
    _, provider = update.callback_query.data.split("--")

    # get price and currency by provider
    currency = PAYMENT_PROVIDERS[provider]["currency"]
    price = await get_price_by_currency(currency)

    # create payment
    bot_user: Bot_user = await get_object_by_update(update)
    payment: Payment = await create_payment(bot_user, price, currency, provider)

    if provider == 'cryptocloud':
        crypto_cloud_sdk = CryptoCloudSDK()
        invoice_data = await crypto_cloud_sdk.create_invoice(payment.pk, price)
        if 'result' in invoice_data:
            link = invoice_data['result']['link']
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=context.words.pay,
                    url=link
                )
            ]])
            text = "invoice"
            await update_message_reply_text(update, text, reply_markup=markup)
    else:
        # send invoice
        title = "Курс"
        description = "Секретная Технология из США (Отабек Одилов)"
        payload = payment.pk
        price = price
        prices = [LabeledPrice("Подписка на канал", int(price * 100))]

        await context.bot.send_invoice(
            chat_id=context._user_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=PAYMENT_PROVIDERS[provider]["token"],
            currency=currency,
            prices=prices,
            start_parameter="payment",
            need_email=True if provider == 'yoomoney' else None,
            send_email_to_provider=True if provider == 'yoomoney' else None,
        )

    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context)


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    # Check the payload to make sure it matches what you sent
    if payment := await get_payment_by_id(query.invoice_payload):
        await payment_pay(payment)
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Something went wrong with the payment.")


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
    await context.bot.send_message(update.effective_user.id, context.words.successful_payment,
                                   reply_markup=markup, parse_mode=ParseMode.HTML)
