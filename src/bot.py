import logging
from config import TELEGRAM_TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters
from get_crypto_info import get_relevant_data

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi! To see available commands, write /help 😊")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """display available commands"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Available commands ⬇️:
/price - to get the current price (in chosen FIAT currency) of a particular cryptocurrency 

/buy - to get the amount of a particular cryptocurrency that could be bought for a particular amount of money (in chosen FIAT currency)

/sell - to get the amount of money (in chosen FIAT currency) that could be received after selling a particular amount of a cryptocurrency 
    """)


async def unknown(update: Update, context: CallbackContext):
    """invalid command"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""Sorry, '{update.message.text}' is not a valid command 😖
Write /help to see the list of available commands 😊
""", reply_to_message_id=update.message.id)


async def unknown_not_command(update: Update, context: CallbackContext):
    """invalid text/not command in user's private chat"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"""Sorry, I didn't understand '{update.message.text}' 😖.
Write /help to see the list of available commands 😊
""", reply_to_message_id=update.message.id)


async def price(update: Update, context: CallbackContext):
    """get info about the current price of a particular crypto"""
    user_text = update.message.text.split()
    error = """Your message must look like this ⬇
️/price cryptocurrency fiat_currency_code"""

    if len(user_text) == 3:  # check if user_input is in a proper format
        # e.g. /price dogecoin usd => ['/price', 'dogecoin', 'usd']
        crypto, fiat_currency = update.message.text.split()[1], update.message.text.split()[2]

        try:
            price_response = get_relevant_data(2, crypto_name=crypto, in_fiat=fiat_currency)
        except KeyError:
            price_response = error

    else:
        price_response = error

    await context.bot.send_message(chat_id=update.effective_chat.id, text=price_response, reply_to_message_id=update.message.id)


async def buy(update: Update, context: CallbackContext):
    """show what amount of a cryptocurrency could be bough for a particular amount of money (FIAT)"""
    user_text = update.message.text.split()
    error = """Your message must look like this ⬇
/buy cryptocurrency fiat_currency_code amount_of_fiat_currency"""

    if len(user_text) == 4:  # check if user_input is in a proper format
        # e.g. /price dogecoin usd => ['/price', 'dogecoin', 'usd', '10']
        crypto, fiat_currency, amount_fiat = update.message.text.split()[1], update.message.text.split()[2], update.message.text.split()[3]

        try:
            buy_response = get_relevant_data(2, crypto_name=crypto, in_fiat=fiat_currency, fiat=float(amount_fiat), buy_or_sell=True)
        except Exception:
            buy_response = error

    else:
        buy_response = error

    await context.bot.send_message(chat_id=update.effective_chat.id, text=buy_response, reply_to_message_id=update.message.id)


async def sell(update: Update, context: CallbackContext):
    """show the amount of money that could be received after selling some crypto"""
    user_text = update.message.text.split()
    error = """Your message must look like this ⬇
/buy cryptocurrency fiat_currency_code amount_of_fiat_currency"""

    if len(user_text) == 4:
        # e.g. /price dogecoin usd => ['/price', 'dogecoin', 'usd', '10']
        crypto, fiat_currency, amount_crypto = update.message.text.split()[1], update.message.text.split()[2], \
                                             update.message.text.split()[3]

        try:
            buy_response = get_relevant_data(2, crypto_name=crypto, in_fiat=fiat_currency, crypto_amount=float(amount_crypto), buy_or_sell=False)
        except Exception:
            buy_response = error

    else:
        buy_response = error

    await context.bot.send_message(chat_id=update.effective_chat.id, text=buy_response,
                                   reply_to_message_id=update.message.id)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # add commands
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    app.add_handler(help_handler)

    price_handler = CommandHandler('price', price)
    app.add_handler(price_handler)

    buy_handler = CommandHandler('buy', buy)
    app.add_handler(buy_handler)

    sell_handler = CommandHandler('sell', sell)
    app.add_handler(sell_handler)

    # invalid commands/text
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    app.add_handler(unknown_handler)

    unknown_not_command_handler = MessageHandler(filters.TEXT, unknown_not_command)
    app.add_handler(unknown_not_command_handler)

    app.run_polling()
