# Import the python-telegram-bot library and the logging module
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import logging
from telegram import Bot
from telegram.utils.request import Request

# Enable logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the bot token and the channel ID to forward posts from
BOT_TOKEN = "6855406193:AAELg2mqIo_BVHcvsk0mAk_YBVCc1PvuffY"
CHANNEL_ID = "@societyoftb"

# Define a list of users who have subscribed to the bot
subscribers = []

# Define a function to handle the /start command
def start(update, context):
    # Send a welcome message to the user
    update.message.reply_text("Introducing our The Logman Telegram Bot By @TheLogman, a one-stop solution for all your CC/DC and Logs needs. This bot is designed to streamline and automate the process of selling CC/DC and Logs, making it easier and more efficient than ever before.")
    # Log the user ID and the command
    logger.info(f"User {update.message.from_user.id} started the bot")

# Define a function to handle the /subscribe command
def subscribe(update, context):
    # Check if the user is already subscribed
    if update.message.from_user.id in subscribers:
        # Send a message saying that the user is already subscribed
        update.message.reply_text("You are already subscribed to the bot.")
    else:
        # Add the user to the subscribers list
        subscribers.append(update.message.from_user.id)
        # Send a confirmation message to the user
        update.message.reply_text("You have successfully subscribed to the bot. You will receive advertisements and forwarded posts from the bot.")
        # Log the user ID and the command
        logger.info(f"User {update.message.from_user.id} subscribed to the bot")

# Define a function to handle the /unsubscribe command
def unsubscribe(update, context):
    # Check if the user is subscribed
    if update.message.from_user.id in subscribers:
        # Remove the user from the subscribers list
        subscribers.remove(update.message.from_user.id)
        # Send a confirmation message to the user
        update.message.reply_text("You have successfully unsubscribed from the bot. You will no longer receive advertisements and forwarded posts from the bot.")
        # Log the user ID and the command
        logger.info(f"User {update.message.from_user.id} unsubscribed from the bot")
    else:
        # Send a message saying that the user is not subscribed
        update.message.reply_text("You are not subscribed to the bot.")

# Define a function to handle the /ad command
def ad(update, context):
    # Check if the user is authorized to send advertisements
    # You can change this condition to suit your needs
    if update.message.from_user.id == 6950394833: # Replace this with the ID of the authorized user
        # Get the text of the advertisement
        ad_text = update.message.text.replace("/ad ", "")
        # Loop through the subscribers list
        for user_id in subscribers:
            try:
                # Send the advertisement to each subscriber
                context.bot.send_message(chat_id=user_id, text=ad_text)
                # Log the user ID and the advertisement
                logger.info(f"Sent advertisement to user {user_id}: {ad_text}")
            except Exception as e:
                # Handle any errors that may occur
                logger.error(f"Failed to send advertisement to user {user_id}: {e}")
        # Send a confirmation message to the sender
        update.message.reply_text("Your advertisement has been sent to all subscribers.")
    else:
        # Send a message saying that the user is not authorized to send advertisements
        update.message.reply_text("You are not authorized to send advertisements.")

# Define a function to handle the channel posts
def channel_post(update, context):
    # Check if the post is from the specified channel
    if update.channel_post.chat_id == CHANNEL_ID:
        # Get the text of the post
        post_text = update.channel_post.text
        # Loop through the subscribers list
        for user_id in subscribers:
            try:
                # Forward the post to each subscriber
                context.bot.forward_message(chat_id=user_id, from_chat_id=CHANNEL_ID, message_id=update.channel_post.message_id)
                # Log the user ID and the post
                logger.info(f"Forwarded post to user {user_id}: {post_text}")
            except Exception as e:
                # Handle any errors that may occur
                logger.error(f"Failed to forward post to user {user_id}: {e}")

# Define a function to handle the unknown commands
def unknown(update, context):
    # Send a message saying that the command is not recognized
    update.message.reply_text("Sorry, I did not understand that command.")

# Create an updater object with the bot token
request = Request(con_pool_size=8) 
bot = Bot(token=BOT_TOKEN, request=request)
updater = Updater(bot=bot, use_context=True)

# Get the dispatcher object from the updater
dispatcher = updater.dispatcher

# Add handlers for the commands and the channel posts
dispatcher.add_handler(CommandHandler('start', start), run_async=True)
dispatcher.add_handler(CommandHandler('subscribe', subscribe))
dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
dispatcher.add_handler(CommandHandler('ad', ad))
dispatcher.add_handler(MessageHandler(filters.update.channel_post, channel_post))
dispatcher.add_handler(MessageHandler(filters.command, unknown))

# Start the bot
updater.start_polling()

# Run the bot until it is manually stopped
updater.idle()
