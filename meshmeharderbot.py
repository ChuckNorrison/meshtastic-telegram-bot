#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to forward Telegram messages to a meshtastic device 

Meshtastic device is used with SerialInterface (USB)

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
meshmeharderbot, forward messages from ADMINs to the mesh.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

# telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#meshtastic
import meshtastic

#helper
from functools import wraps

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# global variables
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
meshtastic_interface = None

# Tweak HERE!
# update path to serial device port
meshtastic_serial = "/dev/ttyUSB0"
# insert token received from your botfather
token = "123123123:xXx"
# Admins are able to send messages to the meshtastic (check your logs for desired telegram user id's)
LIST_OF_ADMINS = [456456456]

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            update.message.reply_text(
                ("tell me more"))
            logger.warning("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    logger.info("User %s found as %d" % (user.mention_markdown_v2(), update.effective_user.id))

# experimental method to show up mesh infos
# this gets printed on console and variables are empty :(
@restricted
def show_command(update: Update, context: CallbackContext) -> None:
    if update.message:
        if update.message.text:
            meshtastic_interface = connect_interface()   

            if meshtastic_interface:
                info = meshtastic_interface.showInfo()
                nodes = meshtastic_interface.showNodes()
                meshtastic_interface.close()
                # update.message.reply_text(info)
                # update.message.reply_text(nodes)
                update.message.reply_text("info gets printed to console (fix me)")
            else:
                update.message.reply_text("Meshtastic interface is missing, try again later")

@restricted
def check_and_forward(update: Update, context: CallbackContext) -> None:
    if update.message:
        if update.message.text and len(update.message.text) > 1:

            # open interface
            meshtastic_interface = connect_interface()

            if meshtastic_interface:
                # trim text to 280bytes
                user_text = (update.message.text[:233] + '..') if len(update.message.text) > 233 else update.message.text

                # sanitize text
                if "/forward" in user_text:
                    user_text = user_text.replace("/forward","")

                if len(user_text)>1:
                    user = update.effective_user
                    if not user['first_name']:
                        meshtastic_interface.sendText("%s: \n%s" % ("unknown", user_text))
                        logger.info("forwarded message\n> %s: \n>> %s" % ("unknown", user_text))
                    else:
                        meshtastic_interface.sendText("%s: \n%s" % (user['first_name'], user_text))
                        logger.info("forwarded message\n> %s: \n>> %s" % (user['first_name'], user_text))

                    update.message.reply_text("SUCCESS: Message forwarded to your meshtastic!")
                else:
                    update.message.reply_text("You should give me a text to forward")

                # close interface
                meshtastic_interface.close()
            else:
                update.message.reply_text("Meshtastic interface is missing, try again later")
        else:
            update.message.reply_text("We can only forward text messages to meshtastic")

def connect_interface() -> None:
    try:
        meshtastic_interface = meshtastic.SerialInterface(meshtastic_serial)
    except:
        meshtastic_interface = None
        logger.error("Meshtastic interface is missing")
    return meshtastic_interface

def error(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    return

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("info", show_command))
    dispatcher.add_handler(CommandHandler("forward", check_and_forward))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_and_forward))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
