from pymongo import MongoClient, errors
import json
from pprint import pprint
import hashlib


def mongoDB_insert_book(_data, _books):
    duplicates = 0  # Кол-во повторов

    for rec in _data:
        # Строка для формирования уникального id
        str_id = rec["Название"].lower() + rec["Категория"].lower()
        rec["_id"] = hashlib.md5(str_id.encode()).hexdigest()

        try:
            _books.insert_one(rec)
        except errors.DuplicateKeyError as e:
            duplicates += 1
    return _books


with open("books_new.json", "r", encoding="utf-8") as file:
    data = json.load(file)

client = MongoClient(host="localhost", port=27017)
db = client["books"]
books = mongoDB_insert_book(data, db.books)

# db.drop_collection("books")

# for doc in books.find({"Категория": "Mystery", "В наличии": 1}):
#     pprint(doc)

# for doc in books.find({"$or": [{"В наличии": {"$gt": 20}}, {"В наличии": {"$lt": 2}}]}):
#     pprint(doc)

# for doc in books.find({"Название": {"$regex": "^Z"}}):
#     pprint(doc)

for rec in books.find({"Название": "Tastes Like Fear (DI Marnie Rome #3)"}):
    pprint(rec)

books.update_one(
    {"Название": "Tastes Like Fear (DI Marnie Rome #3)"},
    {"$set": {"Цена": "15.32"}},
)
print()
for rec in books.find({"Название": "Tastes Like Fear (DI Marnie Rome #3)"}):
    pprint(rec)
