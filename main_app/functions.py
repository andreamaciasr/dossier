from bs4 import BeautifulSoup
import requests
from datetime import datetime


def format_date(url):
    index = url.find("/20")
    date = url[index + 1 : index + 11]
    if date[-1] == "/":
        date = date[:-1]
    elif not date[-1].isdigit():
        date = date[:-2]
    date = date.replace("/", "-")

    return date


def scrapper(query):
    response = requests.get(f"https://www.democracynow.org/topics/{query}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", attrs={"data-ga-action": "Topic: Story Headline"})

        if articles:
            article_list = []
            for article in articles:
                article_dict = {
                    "title": article.text.strip(),
                    "url": "https://www.democracynow.org" + article["href"],
                    "date": format_date(article["href"]),
                }
                article_list.append(article_dict)
            return article_list
        else:
            return "No articles found."
    else:
        return None
