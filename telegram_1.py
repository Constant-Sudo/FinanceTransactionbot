import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
import responses
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater
from config import TOKEN_TELEGRAM as TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Started")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help Message: Use /sent & /received\nExample: /sent €1.363 on Skrill Note: here goes the note")


async def sent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        export = responses.handle_response_tele(update.message)
        # response_str = "Transaction recorded\n\n" + "Date:           " + export[0] +"\n" + 
        # "Time:           " + export[1] + "\n" + "Sent/Received:  " + export[2] + "\n" + 
        # "Amount:         " + export[4] + export[5] + "\n" + "Sent on:        " + export[6] + 
        # "\n" + "Note:           " + export[8] + "\n" +"Who wrote:      " + export[9] + "\n" + "Value:          " + export[10] + "\n"
        response_str = f"""
Transaction recorded\n
Date:                      {export[0]}
Time:                      {export[1]}
Sent/Received:    {export[2]}
Amount:               {export[4]} {export[6]}
Sent on:                {export[7]}
Note:                      {export[8]}
Who wrote:          {export[9]}
Value:                     {export[5]}
"""
        await update.message.reply_text(response_str)
    except Exception as e:
        await update.message.reply_text("Issue accured")
        print("Exception - Received - " + str(e))


async def received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        export = responses.handle_response_tele(update.message)
        # response_str = "Transaction recorded\n\n" + "Date:           " + export[0] + "\n" + "Time:           " + export[1] + "\n" + "Sent/Received:  " + export[2] + "\n" + "Amount:         " + export[4] + export[5] + "\n" + "Sent on:        " + export[6] + "\n" + "Note:           " + export[8] + "\n" +"Who wrote:      " + export[9] + "\n" + "Value:          " + export[10] + "\n"
        response_str = f"""
Transaction recorded\n
Date:                      {export[0]}
Time:                      {export[1]}
Sent/Received:    {export[2]}
Amount:               {export[4]} {export[6]}
Sent on:                {export[7]}
Note:                      {export[8]}
Who wrote:          {export[9]}
Value:                     {export[5]}
"""
        await update.message.reply_text(response_str)
    except Exception as e:
        await update.message.reply_text("Issue accured")
        print("Exception - Received - " + str(e))



def start_bot():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("sent", sent))
    application.add_handler(CommandHandler("received", received))

    # on non command i.e message - echo the message on Telegram

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

    
    # updater = Updater(token)
    # dispatcher = updater.dispatcher
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("send", send))
    # dispatcher.add_handler(CommandHandler("received", received))

    # # Start the bot
    # updater.start_polling()

    # return updater


# def stop_bot


if __name__ == "__main__":
    start_bot()