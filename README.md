# meshtastic-telegram-bot
A simple telegram bot to forward messages to a meshtastic connected device via serial interface

# Dependencies
* A Meshtastic device:
https://github.com/meshtastic/Meshtastic-device

* Meshtastic Android App
https://github.com/meshtastic/Meshtastic-Android

* Meshtastic Python API
https://github.com/meshtastic/Meshtastic-python

* Telegram Python API
https://github.com/python-telegram-bot/python-telegram-bot

# Initial Setup
* Open the bot in a text editor
* Update your bot token 
* Start your bot: `sudo python3 meshmeharderbot.py`
* Write a message to your bot
* Read out the telegram id from console
* Insert your telegram id into LIST_OF_ADMINS

# Basics
Every message send from an admin gets forwarded to the meshtastic
