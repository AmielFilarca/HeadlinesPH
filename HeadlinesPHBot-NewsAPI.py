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
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import requests


# Get functions
def get_top_headlines_entries():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    url = api_keys["Google RSS"]
    NewsFeed = feedparser.parse(url)
    entries = NewsFeed.entries
    return entries


def get_rss_headline(entry):
    try:
        headline = entry.title
        return headline
    except AttributeError:
        return ""


def get_rss_summary(entry):
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


def get_rss_author(entry):
    try:
        author = entry.author
        return author
    except AttributeError:
        return ""


def get_rss_date(entry):
    try:
        date_str = entry.published
        date_dt = parse(date_str)
        date_format = "%a, %d %b %Y @ %I:%M %p"
        manila_tz = date_dt.astimezone(timezone("Asia/Manila"))
        date = manila_tz.strftime(date_format)
        return date
    except AttributeError:
        return ""


def get_rss_link(entry):
    try:
        link = entry.link
        return link
    except AttributeError:
        return ""


def get_rss_image(entry):
    try:
        thisdict = entry.media_content[0]
        media = thisdict["url"]
    except:
        pass
    if not media:
        print("Image: No image available.")
        media = "https://raw.githubusercontent.com/AmielFilarca/HeadlinesPH/master/no_image.png"
        return media
    else:
        print("Image: " + media)
        return media


def get_rss_text(entry):
    news_content = (
        "<b>"
        + get_rss_headline(entry)
        + "</b>"
        + "\n"
        + get_rss_summary(entry)
        + "\n"
        + '<a href="'
        + get_rss_link(entry)
        + '">Read more</a>'
        + "\n"
        + get_rss_author(entry)
        + "\n"
        + get_rss_date(entry)
    )
    print("Title: " + get_rss_headline(entry))
    print("Summary: " + get_rss_summary(entry))
    print("Link: " + get_rss_link(entry))
    print("Source: " + get_rss_author(entry))
    print("Date: " + get_rss_date(entry))
    return news_content


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
    date_format = "%a, %d %b %Y @ %I:%M %p"
    manila_tz = entry_publishedAt_date.astimezone(timezone("Asia/Manila"))
    entry_date = manila_tz.strftime(date_format)
    return str(entry_date)


def get_article_url(entry):
    entry_url = entry["url"]
    return str(entry_url)


def get_cases_dict():
    with open("API-keys.json") as tokens:
        api_keys = json.load(tokens)
    # Get page content
    URL = api_keys["COVID-19"]
    page = requests.get(URL)
    page_content = BeautifulSoup(page.content, "lxml")
    # Init dict
    cases_dict = {
        "cases": "",
        "deaths": "",
        "recovered": "",
        "last_update": "",
        "active_cases": "",
        "mild_condition": "",
        "critical_condition": "",
        "closed_cases": "",
        "recovered_discharged": "",
        "died": "",
    }
    # Get date of last update
    date_div = page_content.find(
        "div", style="font-size:13px; color:#999; text-align:center"
    )
    date_str = date_div.get_text().replace("Last updated:", "")
    date_dt = parse(date_str)
    date_format = "%a, %d %b %Y @ %I:%M %p"
    manila_tz = date_dt.astimezone(timezone("Asia/Manila"))
    date = manila_tz.strftime(date_format)
    cases_dict["last_update"] = date
    # Get main counters data
    counters = page_content.findAll(class_="maincounter-number")
    data = []
    for counter in counters:
        number = counter.find("span").get_text().strip()
        data.append(number)
    # Put main counters data in dict
    cases_dict["cases"] = data[0]
    cases_dict["deaths"] = data[1]
    cases_dict["recovered"] = data[2]
    # Currently Infected Patients & Cases which had an outcome
    num_list = []
    div = page_content.findAll("div", class_="number-table-main")
    for d in div:
        text = d.get_text()
        num_list.append(text)
    cases_dict["active_cases"] = num_list[0]
    cases_dict["closed_cases"] = num_list[1]
    # in Mild Condition & Recovered/Discharged
    left_div = page_content.findAll("div", style="float:left; text-align:center")
    cases_dict["mild_condition"] = left_div[0].get_text().strip().split("\n")[0]
    cases_dict["recovered_discharged"] = " ".join(
        left_div[1].get_text().strip().split("\n")[:2]
    )
    # Serious or Critical & Deaths
    right_div = page_content.findAll("div", style="float:right; text-align:center")
    cases_dict["critical_condition"] = right_div[0].get_text().strip().split("\n")[0]
    cases_dict["died"] = " ".join(right_div[1].get_text().strip().split("\n")[:2])
    # Return dict
    return cases_dict


def get_covid_report():
    cases_dict = get_cases_dict()
    report = (
        "🇵🇭 <b>Philippines</b>"
        + "\n"
        + "• <b>Cases:</b> "
        + cases_dict["cases"]
        + "\n"
        + "• <b>Deaths:</b> "
        + cases_dict["deaths"]
        + "\n"
        + "• <b>Recovered:</b> "
        + cases_dict["recovered"]
        + "\n"
        + "\n"
        + "<b>Active Cases</b>"
        + "\n"
        + cases_dict["active_cases"]
        + " currently infected patients."
        + "\n"
        + cases_dict["mild_condition"]
        + " in mild condition."
        + "\n"
        + cases_dict["critical_condition"]
        + " in serious or critical condition."
        + "\n"
        + "\n"
        + "<b>Closed Cases</b>"
        + "\n"
        + cases_dict["closed_cases"]
        + " cases which had an outcome."
        + "\n"
        + cases_dict["recovered_discharged"]
        + " recovered/discharged."
        + "\n"
        + cases_dict["died"]
        + " deaths."
        + "\n"
        + "\n"
        + "Last updated: "
        + cases_dict["last_update"]
    )
    return report


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
    # * Google RSS
    entries = get_top_headlines_entries()
    entry = entries[random.randrange(len(entries))]
    media = get_rss_image(entry)
    text = get_rss_text(entry)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=media)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True,
    )
    # * News API
    # entries = get_top_headlines_entries()
    # entry = entries[random.randrange(len(entries))]
    # if get_content(entry) == "None":
    #     photo = get_image_url(entry)
    #     message = (
    #         "<b>"
    #         + get_title(entry)
    #         + "</b>"
    #         + "\n"
    #         + "<i>"
    #         + get_description(entry)
    #         + "</i>"
    #         + "\n"
    #         + '<a href="'
    #         + get_article_url(entry)
    #         + '">[Continue reading]</a>'
    #         + "\n"
    #         + get_source(entry)
    #         + "\n"
    #         + get_date(entry)
    #     )
    #     try:
    #         context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text=message,
    #             parse_mode=telegram.ParseMode.HTML,
    #             disable_web_page_preview=True,
    #         )
    #     except:
    #         message = (
    #             "<b>"
    #             + get_title(entry)
    #             + "</b>"
    #             + "\n"
    #             + '<a href="'
    #             + get_article_url(entry)
    #             + '">[Continue reading]</a>'
    #             + "\n"
    #             + get_source(entry)
    #             + "\n"
    #             + get_date(entry)
    #         )
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text=message,
    #             parse_mode=telegram.ParseMode.HTML,
    #             disable_web_page_preview=True,
    #         )

    #     print("Image: " + get_image_url(entry))
    #     print("Title: " + get_title(entry))
    #     print("Description: " + get_description(entry))
    #     print("Content: " + get_content(entry))
    #     print("URL: " + get_article_url(entry))
    #     print("Source: " + get_source(entry))
    #     print("Date: " + get_date(entry))
    #     print("\n")
    # else:
    #     photo = get_image_url(entry)
    #     message = (
    #         "<b>"
    #         + get_title(entry)
    #         + "</b>"
    #         + "\n"
    #         + "<i>"
    #         + get_description(entry)
    #         + "</i>"
    #         + "\n"
    #         + get_content(entry).replace("\n", ". ")
    #         + "\n"
    #         + '<a href="'
    #         + get_article_url(entry)
    #         + '">[Continue reading]</a>'
    #         + "\n"
    #         + get_source(entry)
    #         + "\n"
    #         + get_date(entry)
    #     )
    #     try:
    #         context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text=message,
    #             parse_mode=telegram.ParseMode.HTML,
    #             disable_web_page_preview=True,
    #         )
    #     except:
    #         try:
    #             message = (
    #                 "<b>"
    #                 + get_title(entry)
    #                 + "</b>"
    #                 + "\n"
    #                 + get_content(entry).replace("\n", ". ")
    #                 + "\n"
    #                 + '<a href="'
    #                 + get_article_url(entry)
    #                 + '">[Continue reading]</a>'
    #                 + "\n"
    #                 + get_source(entry)
    #                 + "\n"
    #                 + get_date(entry)
    #             )
    #             context.bot.send_message(
    #                 chat_id=update.effective_chat.id,
    #                 text=message,
    #                 parse_mode=telegram.ParseMode.HTML,
    #                 disable_web_page_preview=True,
    #             )
    #         except:
    #             message = (
    #                 "<b>"
    #                 + get_title(entry)
    #                 + "</b>"
    #                 + "\n"
    #                 + "<i>"
    #                 + get_description(entry)
    #                 + "</i>"
    #                 + "\n"
    #                 + '<a href="'
    #                 + get_article_url(entry)
    #                 + '">[Continue reading]</a>'
    #                 + "\n"
    #                 + get_source(entry)
    #                 + "\n"
    #                 + get_date(entry)
    #             )
    #             context.bot.send_message(
    #                 chat_id=update.effective_chat.id,
    #                 text=message,
    #                 parse_mode=telegram.ParseMode.HTML,
    #                 disable_web_page_preview=True,
    #             )

    #     print("Image: " + get_image_url(entry))
    #     print("Title: " + get_title(entry))
    #     print("Description: " + get_description(entry))
    #     print("Content: " + get_content(entry).replace("\n", ". "))
    #     print("URL: " + get_article_url(entry))
    #     print("Source: " + get_source(entry))
    #     print("Date: " + get_date(entry))
    #     print("\n")


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


# COVID-19
@send_typing_action
def send_covid_report(update, context):
    message = get_covid_report()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True,
    )


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
    dispatcher.add_handler(CommandHandler("covid", send_covid_report))
    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
