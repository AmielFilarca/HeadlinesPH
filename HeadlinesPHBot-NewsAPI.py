import json
import logging
import random
from functools import wraps
import telegram
from telegram import ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
)
from newsapi.newsapi_client import NewsApiClient
from dateutil.parser._parser import parse


# Get functions
def get_top_headlines_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(country="ph")
    entries = top_headlines["articles"]
    return entries


def get_business_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="business", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_entertainment_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="entertainment", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_health_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="health", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_science_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="science", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_sports_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="sports", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_technology_news_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(category="technology", country="ph")
    entries = top_headlines["articles"]
    return entries


def get_custom_news_entries(keyword):
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    newsapi_key = api_keys["NewsAPI"]
    newsapi = NewsApiClient(api_key=newsapi_key)
    top_headlines = newsapi.get_top_headlines(q=keyword, country="ph")
    entries = top_headlines["articles"]
    return entries


def get_image_url(entry):
    entry_urlToImage = entry["urlToImage"]
    return str(entry_urlToImage)


def get_title(entry):
    entry_title = entry["title"]
    return str(entry_title)


def get_description(entry):
    entry_description = entry["description"]
    return str(entry_description)


def get_content(entry):
    entry_content = entry["content"]
    return str(entry_content)


def get_source(entry):
    entry_source = entry["source"]  # {'id': None, 'name': 'Irishmirror.ie'}
    entry_source_name = entry_source["name"]  # Irishmirror.ie
    return str(entry_source_name)


def get_date(entry):
    entry_publishedAt = entry["publishedAt"]
    entry_publishedAt_date = parse(entry_publishedAt)
    entry_date = entry_publishedAt_date.strftime("%a, %d %b %Y @ %I:%M %p")
    return str(entry_date)


def get_article_url(entry):
    entry_url = entry["url"]
    return str(entry_url)


# Send functions
def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


# Start
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Headlines PH provides you with the latest news updates from the most popular news sources in the Philippines. \nUse the commands to get news from different categories. \nUse '<b>/search</b> <i>keyword</i>' to search for articles.",
        parse_mode=telegram.ParseMode.HTML,
    )


# Top headlines
@send_typing_action
def send_top_headline(update, context):
    entries = get_top_headlines_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Business
@send_typing_action
def send_business_news(update, context):
    entries = get_business_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Entertainment
@send_typing_action
def send_entertainment_news(update, context):
    entries = get_entertainment_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Health
@send_typing_action
def send_health_news(update, context):
    entries = get_health_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Science
@send_typing_action
def send_science_news(update, context):
    entries = get_science_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Sports
@send_typing_action
def send_sports_news(update, context):
    entries = get_sports_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Technology
@send_typing_action
def send_technology_news(update, context):
    entries = get_technology_news_entries()
    entry = entries[random.randrange(len(entries))]
    if get_content(entry) == "None":
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")
    else:
        photo = get_image_url(entry)
        message = (
            "<b>"
            + get_title(entry)
            + "</b>"
            + "\n"
            + "<i>"
            + get_description(entry)
            + "</i>"
            + "\n"
            + get_content(entry).replace("\n", ". ")
            + "\n"
            + '<a href="'
            + get_article_url(entry)
            + '">[Continue reading]</a>'
            + "\n"
            + get_source(entry)
            + "\n"
            + get_date(entry)
        )
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except:
            try:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + get_content(entry).replace("\n", ". ")
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + "<i>"
                    + get_description(entry)
                    + "</i>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

        print("Image: " + get_image_url(entry))
        print("Title: " + get_title(entry))
        print("Description: " + get_description(entry))
        print("Content: " + get_content(entry).replace("\n", ". "))
        print("URL: " + get_article_url(entry))
        print("Source: " + get_source(entry))
        print("Date: " + get_date(entry))
        print("\n")


# Search
@send_typing_action
def send_custom_news(update, context):
    keyword = " ".join(context.args)
    entries = get_custom_news_entries(keyword)
    if not entries:
        crying_cats = [
            "https://i.kym-cdn.com/photos/images/original/001/384/531/8ed.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/384/542/f03.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/384/550/69b.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/510/490/e7f.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/389/470/b3b.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/389/464/318.png",
            "https://i.kym-cdn.com/photos/images/original/001/384/543/865.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/384/545/7b9.jpg",
            "https://i.kym-cdn.com/photos/images/original/001/384/535/295.jpg",
            "https://i.kym-cdn.com/photos/images/newsfeed/001/481/456/1f2.gif",
            "https://i.kym-cdn.com/photos/images/original/001/384/541/1d8.jpg",
        ]
        image = crying_cats[random.randrange(len(crying_cats))]
        if image[len(image) - 3 : len(image)] == "gif":
            context.bot.send_animation(
                chat_id=update.effective_chat.id, animation=image
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="<b>No result for</b> '" + str(keyword) + "'",
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        else:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="<b>No result for</b> '" + str(keyword) + "'",
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
    else:
        entry = entries[random.randrange(len(entries))]
        if get_content(entry) == "None":
            photo = get_image_url(entry)
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + "<i>"
                + get_description(entry)
                + "</i>"
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            try:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                message = (
                    "<b>"
                    + get_title(entry)
                    + "</b>"
                    + "\n"
                    + '<a href="'
                    + get_article_url(entry)
                    + '">[Continue reading]</a>'
                    + "\n"
                    + get_source(entry)
                    + "\n"
                    + get_date(entry)
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )

            print("Image: " + get_image_url(entry))
            print("Title: " + get_title(entry))
            print("Description: " + get_description(entry))
            print("Content: " + get_content(entry))
            print("URL: " + get_article_url(entry))
            print("Source: " + get_source(entry))
            print("Date: " + get_date(entry))
            print("\n")
        else:
            photo = get_image_url(entry)
            message = (
                "<b>"
                + get_title(entry)
                + "</b>"
                + "\n"
                + "<i>"
                + get_description(entry)
                + "</i>"
                + "\n"
                + get_content(entry).replace("\n", ". ")
                + "\n"
                + '<a href="'
                + get_article_url(entry)
                + '">[Continue reading]</a>'
                + "\n"
                + get_source(entry)
                + "\n"
                + get_date(entry)
            )
            try:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=message,
                    parse_mode=telegram.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                try:
                    message = (
                        "<b>"
                        + get_title(entry)
                        + "</b>"
                        + "\n"
                        + get_content(entry).replace("\n", ". ")
                        + "\n"
                        + '<a href="'
                        + get_article_url(entry)
                        + '">[Continue reading]</a>'
                        + "\n"
                        + get_source(entry)
                        + "\n"
                        + get_date(entry)
                    )
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except:
                    message = (
                        "<b>"
                        + get_title(entry)
                        + "</b>"
                        + "\n"
                        + "<i>"
                        + get_description(entry)
                        + "</i>"
                        + "\n"
                        + '<a href="'
                        + get_article_url(entry)
                        + '">[Continue reading]</a>'
                        + "\n"
                        + get_source(entry)
                        + "\n"
                        + get_date(entry)
                    )
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True,
                    )

            print("Image: " + get_image_url(entry))
            print("Title: " + get_title(entry))
            print("Description: " + get_description(entry))
            print("Content: " + get_content(entry).replace("\n", ". "))
            print("URL: " + get_article_url(entry))
            print("Source: " + get_source(entry))
            print("Date: " + get_date(entry))
            print("\n")


# Main
def main():
    # Telegram token
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    token = api_keys["NewsPH"]
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    # Logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("news", send_top_headline))
    dispatcher.add_handler(CommandHandler("business", send_business_news))
    dispatcher.add_handler(CommandHandler("entertainment", send_entertainment_news))
    dispatcher.add_handler(CommandHandler("health", send_health_news))
    dispatcher.add_handler(CommandHandler("science", send_science_news))
    dispatcher.add_handler(CommandHandler("sports", send_sports_news))
    dispatcher.add_handler(CommandHandler("technology", send_technology_news))
    dispatcher.add_handler(CommandHandler("search", send_custom_news))
    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
