from bot.bot import *
import json
import logging
import traceback
import html


async def start(update: Update, context: CustomContext):
    # get or create bot user
    bot_user: Bot_user = await get_or_create(update.effective_user.id)
    
    # send first message
    text = Strings.hello
    url=f"{WEBAPP_URL}/view-video"
    i_button = InlineKeyboardButton(text=context.words.view_video, url=url)
    markup = InlineKeyboardMarkup([[i_button]])
    await context.bot.send_message(update.message.chat_id, text, reply_markup=markup)
    # create job queue to send alert if not shown video yet



async def newsletter_update(update: NewsletterUpdate, context: CustomContext):
    bot = context.bot
    if not (update.photo or update.video or update.document):
        # send text message
        message = await bot.send_message(
            chat_id=update.user_id,
            text=update.text,
            reply_markup=update.reply_markup,
            parse_mode=ParseMode.HTML
        )

    if update.photo:
        # send photo
        message = await bot.send_photo(
            update.user_id,
            update.photo,
            caption=update.text,
            reply_markup=update.reply_markup,
            parse_mode=ParseMode.HTML,
        )
    if update.video:
        # send video
        message = await bot.send_video(
            update.user_id,
            update.video,
            caption=update.text,
            reply_markup=update.reply_markup,
            parse_mode=ParseMode.HTML,
        )
    if update.document:
        # send document
        message = await bot.send_document(
            update.user_id,
            update.document,
            caption=update.text,
            reply_markup=update.reply_markup,
            parse_mode=ParseMode.HTML,
        )
    if update.pin_message:
        await bot.pin_chat_message(chat_id=update.user_id, message_id=message.message_id)


###############################################################################################
###############################################################################################
###############################################################################################
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CustomContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=206261493, text=message, parse_mode=ParseMode.HTML
    )
