import requests
from lxml import html
from datetime import datetime
import csv
import sys

url = "https://news.mail.ru/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (HTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


# Извлечение информации со страницы
def get_news_info(_url):
    data = {}
    print(f"парсинг страницы: {_url}")

    try:
        response = requests.get(_url, headers=headers)
    except Exception as err:
        print(f"ошибка: {err}")
        return None
    if not response.ok:
        print(f"Ошибка: {response.status_code}")
        return None

    dom = html.fromstring(response.text)
    # Дата и время публикации
    date_time = dom.xpath("//div[@data-article-index='0']//time/@datetime")

    # Заголовок
    title = dom.xpath("//div[@data-article-index='0']//h1/text()")

    # Короткое описание
    short_text = dom.xpath(
        "//div[@data-article-index='0']//div[@data-qa='Text']/p/text()"
    )
    # Основной текст
    text = dom.xpath(
        "//div[@data-article-index='0']//div[@article-item-type='html']//text()"
    )

    try:
        data["Дата_время"] = datetime.fromisoformat("".join(date_time))
    except:
        data["Дата_время"] = ""
    data["Заголовок"] = "".join(title).replace("\xa0", " ")
    data["Краткая_инфо"] = "".join(short_text).replace("\xa0", " ")
    data["Текст"] = " ".join(text).replace("\xa0", " ")
    return data


print(f"парсинг страницы: {url}")
try:
    response = requests.get(url, headers=headers)
except Exception as err:
    print("Выполнение кода прервано")
    print(f"Ошибка: {err}")
    sys.exit(1)

if not response.ok:
    print("Выполнение кода прервано")
    print(f"Ошибка: {response.status_code}")
    sys.exit(1)

dom = html.fromstring(response.text)

# Поиск всех ссылок на новости
links = dom.xpath("//div[@class='js-module']//a/@href")

# Удаляем повторные (скрытые) ссылки (две ссылки на одну новости даны для разной ширины экрана)
links = list(set(links))

news = []
for link in links:
    news.append(get_news_info(link))
print(f"парсинг завершен")

filename = "mail-news.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=news[0].keys())
    writer.writeheader()
    writer.writerows(news)
print(f"csv-файл сохранен")
