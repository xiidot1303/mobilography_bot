from bot.bot import *
from app.services.price_service import *
from app.services.payment_service import *
from app.services.price_service import *
from payment.services.cryptocloud_service import *


async def get_payment_provider(update: Update, context: CustomContext):
    _, provider = update.callback_query.data.split("--")
    i_button = InlineKeyboardButton(
        text=context.words.change_payment_method,
        callback_data="change_payment_method"
    )
    new_markup = InlineKeyboardMarkup([[i_button]])
    if provider == "global":
        text = """Из-за санкций в РФ платежные системы не принимают оплаты через Visa / Mastercard 
        
В связи с этим мы вынуждены принимать оплаты на визу карту: 

4998930007821600
Odilov Otabek

после оплаты отправьте чек в этот @konkretno_production тг и вам отправят доступ"""

        await bot_edit_message_reply_markup(update, context, reply_markup=new_markup)
        await context.bot.send_message(update.effective_user.id, text)
        return

    bot_user: Bot_user = await get_object_by_update(update)
    # get price and currency by provider
    currency = PAYMENT_PROVIDERS[provider]["currency"]
    price = await get_price_by_id_and_currency(bot_user.price_id, currency)

    # create payment
    payment: Payment = await create_payment(bot_user, price, currency, provider, bot_user.price_id)

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

        PROVIDER_DATA_WO_EMAIL = {
            "receipt": {
                "items": [{
                    "description": "Секретная Технология из США (Отабек Одилов)",
                    "quantity": 1,
                    "amount": {
                        "value": price,
                        "currency": "RUB"
                    },
                    "vat_code": 1,
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity"
                }],
            }
        }

        await context.bot.send_invoice(
            chat_id=context._user_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=PAYMENT_PROVIDERS[provider]["token"],
            currency=currency,
            prices=prices,
            start_parameter="payment",

            # yoomoney
            provider_data=PROVIDER_DATA_WO_EMAIL if provider == 'yoomoney' else None,
            need_email=True if provider == 'yoomoney' else None,
            send_email_to_provider=True if provider == 'yoomoney' else None,
        )

    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context, reply_markup=new_markup)


async def change_payment_method(update: Update, context: CustomContext):
    try:
        await bot_edit_message_reply_markup(update, context)
    except:
        None

    text = context.words.choose_payment_method
    markup = payment_providers_keyboard
    await update_message_reply_text(update, text, markup)


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

    price: Price = await get_price_by_id(bot_user.price_id)
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text=context.words.join_channel,
            url=price.channel_join_link
        )
    ]])
    await context.bot.send_message(update.effective_user.id, context.words.successful_payment,
                                   reply_markup=markup, parse_mode=ParseMode.HTML)
