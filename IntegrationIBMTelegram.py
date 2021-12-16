import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wiotp.sdk.device
import time
import random


myConfig = { 
    "identity": {
        "orgId": "3cfp21",
        "typeId": "NodeMCU",
        "deviceId":"54321"
    },
    "auth": {
        "token": "12345678"
    }
}

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


he = 'Type below commands to execute \ntemperature - to get Temperature Data \nLight Intensity - to get Light Intensity Data \nhumidity - to get Humdity Data \nLight On - to Switch On the Light \nLight Off - to Switch Off the Light \n'
def echo(update, context):
    """Echo the user message."""
    k = update.message.text
    k = k.lower()
    if k == 'commands':
        update.message.reply_text(h)
    elif k == 'temperature':
        t = random.randint(0,100)
        update.message.reply_text('Current Temperature is ' + str(t))
    elif k == 'humidity':
        h = random.randint(0,100)
        update.message.reply_text('Current Humidity is ' + str(h))
    elif k == 'Light Intensity':
        l = random.randint(100,300)
        update.message.reply_text('Current Light Intensity is ' + str(l))
    elif k == 'light on':
        update.message.reply_text('Light is Switched On')
    elif k == 'light off':
        update.message.reply_text('Light is Switched Off')
                                  
    else:
        update.message.reply_text('Invalid!\n' + he)
    print(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("2119454279:AAFTs5QjhYAstHvOVnHj0GUl3Cyz7JSGTjU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    while True:
        temp=random.randint(0,100)
        hum=random.randint(0,100)
        li=random.randint(100,300)
        myData={'Temperature':temp, 'Humidity':hum, 'LightIntensity':li}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", myData)
        client.commandCallback = myCommandCallback
        time.sleep(2)
        updater.start_polling()
    #print(updater.start_polling())
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    print("main")

if __name__ == '__main__':
    print("start")
    main()

client.disconnect()







