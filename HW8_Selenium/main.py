from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


options = Options()
options.add_argument("start-maximized")

# Установка веб-драйвера
driver = webdriver.Chrome(options=options)
# Переход на веб-сайт
driver.get("https://market.yandex.ru/")

# Поиск строки поиска
input = driver.find_element(By.ID, "header-search")
# Отправка запроса
product_name = "квадроцикл"
input.send_keys(product_name)
input.submit()


while True:
    # Проверка прогрузки страницы
    wait = WebDriverWait(driver, timeout=10)
    cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//article[@data-auto='searchOrganic']")
        )
    )
    count = len(cards)
    # Прокрутить вниз
    driver.execute_script("window.scrollBy(0, 2000)")
    time.sleep(2)
    cards = driver.find_elements(By.XPATH, "//article[@data-auto='searchOrganic']")
    if len(cards) == count:
        break


data = []
for card in cards:
    try:
        price = card.find_element(
            By.XPATH, ".//span[@data-auto='snippet-price-current']"
        ).text
        name = card.find_element(By.XPATH, ".//span[@itemprop='name']").text
        url = card.find_element(By.XPATH, ".//div//a").get_attribute("href")
        print(name, price, url)
        data.append([price, name, url])
    except Exception as e:
        print("Ошибка при извлечении данных:", e)

with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
print("Данные записаны в data.json")
driver.quit()
