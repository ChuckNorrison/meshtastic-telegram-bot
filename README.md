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
* Start your bot: `python3 meshmeharderbot.py`
* Write a message to your bot
* Read out the telegram id from console
* Insert your telegram id into LIST_OF_ADMINS

# Basics
Every telegram message send from an admin gets forwarded to the meshtastic
You can add the bot to a group and forward messages within the group with /forward <text>
Messages which exceeds payload size gets stripped down automatically. 

## FAQ/common problems

This is a collection of common questions and answers from our friendly forum.

### [Permission denied: ‘/dev/ttyUSB0’](https://meshtastic.discourse.group/t/question-on-permission-denied-dev-ttyusb0/590/3?u=geeksville)

This indicates an OS permission problem for access by your user to the USB serial port.  Typically this is fixed by the following.

Some Linux commands to overcome this issue:
  
Method 1: Add your user to the group dialout
```
sudo usermod -a -G dialout <username>
```

Method 2: Another try would be to take ownership of this interface
```
sudo su
cd /dev
chown <username> ttyUSB0
exit
```
  
Method 3: Last you can also start your telegram bot as root
```
sudo python3 meshmeharderbot.py
```
