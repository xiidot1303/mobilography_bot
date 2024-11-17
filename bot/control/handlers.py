from bot import *
from bot.resources.conversationList import *

from bot.bot import (
    main, payment
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(Strings.main_menu))

start = CommandHandler('start', main.start)

handlers = [
    start,
    TypeHandler(type=NewsletterUpdate, callback=main.newsletter_update),
    CallbackQueryHandler(payment.get_payment_provider, pattern=".*payment_provider.*"),
    PreCheckoutQueryHandler(payment.precheckout_callback),
    MessageHandler(filters.SUCCESSFUL_PAYMENT, payment.successful_payment),
]