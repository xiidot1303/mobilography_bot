from bot.bot import *


async def channel_join_request(update: Update, context: CustomContext):
    # check user already has access to channel
    bot_user: Bot_user = await get_object_by_update(update)
    if bot_user.has_access_to_channel:
        await update.chat_join_request.approve()
        text = context.words.successfully_joined
        await context.bot.send_message(context._user_id, text)
        return
