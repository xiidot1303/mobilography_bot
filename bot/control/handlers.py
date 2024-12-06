from bot import *
from bot.resources.conversationList import *

from bot.bot import (
    main, payment, join_request
)

exceptions_for_filter_text = (~filters.COMMAND) & (
    ~filters.Text(Strings.main_menu))

start = CommandHandler('start', main.start)
channel_join_request_handler = ChatJoinRequestHandler(
    join_request.channel_join_request)

successfully_payment_handler = MessageHandler(
    filters.SUCCESSFUL_PAYMENT, payment.successful_payment)

handlers = [
    start,
    TypeHandler(type=NewsletterUpdate, callback=main.newsletter_update),
    CallbackQueryHandler(payment.get_payment_provider,
                         pattern=".*payment_provider.*"),
    PreCheckoutQueryHandler(payment.precheckout_callback),
    successfully_payment_handler,
    channel_join_request_handler,
]
