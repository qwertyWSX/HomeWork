import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://books.toscrape.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (HTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


# Получить все категории
def get_categories():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    navbar = soup.find("ul", {"class": "nav nav-list"}).find_all("a")

    category = {}
    for row in navbar[1:]:
        category[row.getText().strip()] = url + row.get("href")
    return category


# Получить все ссылки на книги в категории
def get_book_links(_url):
    links = []
    link_path = url + "catalogue/"

    while True:
        response = requests.get(_url, headers=headers)
        page_path = _url
        if not response.ok:
            return response.status_code
        soup = BeautifulSoup(response.text, features="html.parser")
        container = soup.find_all("article", {"class": "product_pod"})

        for data in container:
            links.append(link_path + data.find("a").get("href")[9:])

        next_page = soup.find("li", {"class": "next"})
        if next_page is None:
            return links
        else:
            _url = page_path[: page_path.rfind("/") + 1] + next_page.find("a").get(
                "href"
            )


# Получить информацию о книге
def get_book_info(_url):
    response = requests.get(_url, headers=headers)
    response.encoding = "utf-8"
    if not response.ok:
        return response.status_code
    soup = BeautifulSoup(response.text, features="html.parser")
    title = (
        soup.find("div", {"class": "col-sm-6 product_main"})
        .find("h1")
        .get_text(strip=True)
    )
    price = soup.find("p", {"class": "price_color"}).get_text(strip=True)

    available = soup.find("p", {"class": "instock availability"}).get_text(strip=True)
    available = re.search(r"\(\s*(\d+)\s*available\)", available).group(1)
    available = int(available) if available else 0

    describe = soup.find("div", {"id": "product_description"})
    if describe:
        describe = describe.find_next_sibling("p").get_text()
    else:
        describe = ""

    return {
        "Название": title,
        "Цена": price,
        "В наличии": available,
        "Описание": describe,
    }


books = {}
links = {}
categories = get_categories()

iter = 1
for cat, link in categories.items():
    print(iter, link)
    links[cat] = get_book_links(link)
    iter = iter + 1
print()

iter = 1
for cat, lst in links.items():
    books[cat] = []
    for l in lst:
        print(iter, l)
        books[cat].append(get_book_info(l))
        iter = iter + 1

print("Сохранение в Json-файл")
with open("books.json", "w", encoding="utf-8") as file:
    json.dump(books, file, ensure_ascii=False, indent=4)
print("Сохранение завершено")
