# Import the python-telegram-bot library and the logging module
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

# Enable logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the bot token and the channel ID to forward posts from
BOT_TOKEN = "6855406193:AAELg2mqIo_BVHcvsk0mAk_YBVCc1PvuffY"
CHANNEL_ID = "societyoftb"

# Define a list of users who have subscribed to the bot
subscribers = []

# Create an updater object with the bot token
updater = Updater(token=BOT_TOKEN, use_context=True)

# Authorized user ID for checking subscriber count
AUTHORIZED_USER_ID = 6950394833  # Replace with the actual authorized user ID

# Get the dispatcher object from the updater
dispatcher = updater.dispatcher

# Define a function to handle the /start command
def start(update, context):
    keyboard = [[InlineKeyboardButton("Subscribe", callback_data='subscribe')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Introducing our The Logman Telegram Bot By @TheLogman, a one-stop solution for all your CC/DC and Logs needs. This bot is designed to streamline and automate the process of selling CC/DC and Logs, making it easier and more efficient than ever before. Click the button below to subscribe.", reply_markup=reply_markup)

# Define a function to handle the /subscribe command and button
def subscribe(update, context):
    user_id = update.effective_user.id
    if user_id not in subscribers:
        subscribers.append(user_id)
        context.bot.send_message(
            chat_id=user_id,
            text="You have successfully subscribed to the bot."
        )
        logger.info(f"User {user_id} subscribed to the bot")
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="You are already subscribed to the bot."
        )

# Define a function to handle the /unsubscribe command
def unsubscribe(update, context):
    user_id = update.effective_user.id
    if user_id in subscribers:
        subscribers.remove(user_id)
        update.message.reply_text("You have successfully unsubscribed from the bot.")
        logger.info(f"User {user_id} unsubscribed from the bot")
    else:
        update.message.reply_text("You are not subscribed to the bot.")

# Define a function to handle the /check_subscribers command
def check_subscribers(update, context):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        update.message.reply_text(f"The bot currently has {len(subscribers)} subscribers.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Define a function to handle button presses
def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'subscribe':
        subscribe(query, context)

# Define a function to handle the /ad command
def ad(update, context):
    if update.effective_user.id == AUTHORIZED_USER_ID: # Replace this with the ID of the authorized user
        update.message.reply_text("Please send the content of the advertisement.")
        return 'WAITING_FOR_AD_CONTENT'
    else:
        update.message.reply_text("You are not authorized to send advertisements.")
        return ConversationHandler.END

# Define a function to handle the advertisement content
def ad_content(update, context):
    user_id = update.effective_user.id
    if update.message.photo:
        photo_file = update.message.photo[-1].get_file()
        caption = update.message.caption
        for sub_id in subscribers:
            try:
                context.bot.send_photo(chat_id=sub_id, photo=photo_file, caption=caption)
                logger.info(f"Sent photo advertisement to user {sub_id}")
            except Exception as e:
                logger.error(f"Failed to send photo advertisement to user {sub_id}: {e}")
    else:
        ad_text = update.message.text
        for sub_id in subscribers:
            try:
                context.bot.send_message(chat_id=sub_id, text=ad_text)
                logger.info(f"Sent text advertisement to user {sub_id}: {ad_text}")
            except Exception as e:
                logger.error(f"Failed to send text advertisement to user {sub_id}: {e}")
    update.message.reply_text("Your advertisement has been sent to all subscribers.")
    return ConversationHandler.END

# Create a conversation handler for the /ad command and the advertisement content
def cancel(update, context):
    update.message.reply_text("You have cancelled the conversation.")
    logger.info(f"User {update.effective_user.id} cancelled the conversation")
    return ConversationHandler.END

ad_handler = ConversationHandler(
    entry_points=[CommandHandler('ad', ad)],
    states={
        'WAITING_FOR_AD_CONTENT': [
            MessageHandler(Filters.text & ~Filters.command, ad_content),
            MessageHandler(Filters.photo & ~Filters.command, ad_content)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('subscribe', subscribe))
dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
dispatcher.add_handler(CommandHandler('check_subscribers', check_subscribers))
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(ad_handler)

# Other handlers and functions here...

# Start the bot
updater.start_polling()

# Run the bot until it is manually stopped
updater.idle()
