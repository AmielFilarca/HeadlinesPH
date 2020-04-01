import feedparser
from bs4 import BeautifulSoup
import random


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
        return "There is no such attribute."


def get_image(entry):
    try:
        thisdict = entry.media_content[0]
        media = thisdict["url"]
        return media
    except AttributeError:
        return "There is no such attribute."


def get_summary(entry):
    try:
        html = entry.summary
        parsed_html = BeautifulSoup(html, features="html.parser")
        summary = parsed_html.find("div").text
        if summary == "":
            src = parsed_html.find("iframe").get("src")
            summary = src
        return summary
    except AttributeError:
        return "There is no such attribute."


def get_author(entry):
    try:
        author = entry.author
        return author
    except AttributeError:
        return "There is no such attribute."


def get_date(entry):
    try:
        date = entry.published
        return date
    except AttributeError:
        return "There is no such attribute."


def get_news_content(entry):
    news_content = (
        get_headline(entry)
        + "\n"
        + get_image(entry)
        + "\n"
        + get_summary(entry)
        + "\n"
        + get_author(entry)
        + "\n"
        + get_date(entry)
        + "\n"
    )
    return news_content


def print_all_entries():
    entries = get_entries()
    for entry in entries:
        news_content = get_news_content(entry)
        print(news_content)


def print_random_entry():
    entries = get_entries()
    number_of_entries = len(entries)
    entry_index = random.randint(0, number_of_entries)
    entry = entries[entry_index]
    news_content = get_news_content(entry)
    print(news_content)


def print_top_entry():
    entries = get_entries()
    entry = entries[0]
    news_content = get_news_content(entry)
    print(news_content)


def print_number_of_entries(limit):
    entries = get_entries()
    entries = entries[:limit]
    for entry in entries:
        news_content = get_news_content(entry)
        print(news_content)


def run_command(command):
    switcher = {
        "/news": print_top_entry,
        "/random": print_random_entry,
        "/all": print_all_entries,
    }
    function = switcher.get(command, lambda: print("Invalid command"))
    function()


def check_command(command):
    return " " in command


def run_special_command(command):
    commands = command.split(" ")
    commands[1] = int(commands[1])
    if commands[0] == "/news":
        if commands[1] > 0:
            limit = commands[1]
            print_number_of_entries(limit)
        else:
            print("Invalid command")
    else:
        print("Invalid command")


def main():
    command = input("Enter a command: ")
    if check_command(command):
        run_special_command(command)
    else:
        run_command(command)


if __name__ == "__main__":
    main()
