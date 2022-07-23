# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from import_DB import create_companies_DB
from import_DB import find_companies
import logging
#
# from telegram import __version__ as TG_VER
#
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
#
# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
from telegram import ForceReply, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I will help you find the sponsors of terrorism carried out by Russia!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Enter the name of the trademark or legal entity, and I will check their involvement in the sponsorship of terrorism carried out by Russia!")


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text
    result = find_companies(msg)
    if result != None: await update.message.reply_text('{}: founded result - {}'.format(msg, str(result[0])))
    else: await update.message.reply_text("No results found")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if query == "":
        print("Empty query")
        return
    print("Non empty query:", query)
    result = find_companies(str(query))
    if result != None:
        print("Result of query:", result[0])
        results = [
            InlineQueryResultArticle(
                id="1",
                title=query,
                input_message_content=InputTextMessageContent(result[0]),
                description="found",
            ),
        ]
    else:
        result = "Query is empty"
        print(result)
        results = [
            InlineQueryResultArticle(
                id="2",
                title=query,
                input_message_content=InputTextMessageContent("Not found!"),
                description="not found",
            ),
        ]

    print(str(query))
    await update.inline_query.answer(results)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5311505435:AAGMgr1KjAF6AQtBRGKGB2rI_j3MCis3vbA").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - find the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find))
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    #create_companies_DB()
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
