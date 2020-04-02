import json
import logging
import feedparser
from bs4 import BeautifulSoup
import random
from functools import wraps
import telegram
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
)


# Get
def get_entries():
    url = "https://rss.app/feeds/06baSi0bagPEqNTP.xml"
    NewsFeed = feedparser.parse(url)
    entries = NewsFeed.entries
    return entries


def get_headline(entry):
    try:
        headline = entry.title
        return headline
    except AttributeError:
        return ""


def get_image(entry):
    try:
        thisdict = entry.media_content[0]
        media = thisdict["url"]
        return media
    except AttributeError:
        return ""


def get_summary(entry):
    try:
        html = entry.summary
        parsed_html = BeautifulSoup(html, features="html.parser")
        summary = parsed_html.find("div").text
        if summary == "":
            src = parsed_html.find("iframe").get("src")
            summary = "Watch: " + src
        return summary
    except AttributeError:
        return ""


def get_author(entry):
    try:
        author = "\n" + entry.author
        return author
    except AttributeError:
        return ""


def get_date(entry):
    try:
        date = "\n" + entry.published
        return date
    except AttributeError:
        return ""


def get_link(entry):
    try:
        link = entry.link
        return link
    except AttributeError:
        return ""


def get_media(entry):
    news_content = get_image(entry)
    return news_content


def get_text(entry):
    news_content = (
        "<b>"
        + get_headline(entry)
        + "</b>"
        + "\n"
        + get_summary(entry)
        + "<i>"
        + get_author(entry)
        + "</i>"
        + get_date(entry)
        + "\n"
        + '<a href="'
        + get_link(entry)
        + '">Read more</a>'
    )
    return news_content


# Send
def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


@send_typing_action
def start(update, context):
    reply_markup = keyboard()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Headlines PH provides you with the latest news updates from the most popular news sources in the Philippines.",
        reply_markup=reply_markup,
    )


@send_typing_action
def send_news(update, context):
    entries = get_entries()
    number_of_entries = len(entries) - 1
    entry_index = random.randint(0, number_of_entries)
    entry = entries[entry_index]
    media = get_media(entry)
    text = get_text(entry)
    reply_markup = keyboard()
    if media:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=media)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )


@send_typing_action
def send_latest(update, context):
    entries = get_entries()
    entry = entries[0]
    media = get_media(entry)
    text = get_text(entry)
    reply_markup = keyboard()
    if media:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=media)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )


# Keyboard
def keyboard():
    keyboard = [
        [
            InlineKeyboardButton("News", callback_data="News"),
            InlineKeyboardButton("Latest article", callback_data="Latest article"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# Bot
def main():
    # Get token
    with open("Token.json") as tokens:
        dict_tokens = json.load(tokens)
    token = dict_tokens["NewsPH"]
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    # Logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # Command handlers
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    news_handler = CommandHandler("news", send_news)
    dispatcher.add_handler(news_handler)
    latest_handler = CommandHandler("latest", send_latest)
    dispatcher.add_handler(latest_handler)
    updater.dispatcher.add_handler(
        CallbackQueryHandler(send_news, pattern="^" + "News" + "$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(send_latest, pattern="^" + "Latest article" + "$")
    )
    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
