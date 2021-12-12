import json
import random
import os

from faker import Faker

import conf

CONFIG_PATHFILE = "conf.py"
BOOK_TITLES_PATHFILE = "books.txt"
JSON_PATHFILE = "generated_books.json"

def dict_book_generator(pk : int = 1) -> iter:
    """
    Генератор словарей для книг
    :param pk: arg1, по умолчанию 1
    :type pk: int

    :rtype: iter
    :return: словарь, описывающий случайно сгенерированную книгу
    """

    while True:
        book = {
            "model" : get_model_title_from_conf_file(),
            "pk" : pk,
            "fields": get_book_fields()
        }

        pk += 1

        yield book


def get_model_title_from_conf_file() -> str:
    """
    Извлечения названия модели из файла conf.py
    :rtype: str
    :return: название модели из конфигурационного файла
    """

    model_title = conf.model

    return model_title


def get_book_fields() -> dict:
    """
    Генерация словаря для случайной книги
    :rtype: dict
    :return: словарь, описывающий поля случайно сгенерированной книги
    """

    book_fields = {
        "title":    get_title_from_file(),
        "year":     get_year(),
        "pages":    get_page_count(),
        "isbn13":   get_isbn(),
        "rating":   get_rating(),
        "price":    get_price(),
        "discount": get_discount(),
        "author":   get_author_list()
    }

    return book_fields


def get_title_from_file() -> str:
    """
    Извлечение случайного названия книги из файла books.txt (5 названий на русском с новой строки)
    :rtype: str
    :return: случайное название для книги из файла books.txt
    """

    # Похоже, можно выкинуть в декоратор создание файла при отсутствии
    if os.path.exists(BOOK_TITLES_PATHFILE):
        with open(BOOK_TITLES_PATHFILE, "r") as book_titles_file:
            book_titles_list = book_titles_file.readlines()
    else:
        with open(BOOK_TITLES_PATHFILE, "w+") as book_titles_file:
            print("Названий нет, пишем")
            book_titles_list = ["Мёртвые души\n", "Моби Дик\n", "Хазарский словарь\n", "В чаще\n", "Сон\n"]
            book_titles_file.writelines(book_titles_list)

    book_title = random.choice(book_titles_list)

    book_title = book_title.strip('\n')

    return book_title


def get_year() -> int:
    """
    Генерация случайного года
    :rtype: int
    :return: случайный год для книги (от 1400 до 2022)
    """

    year = random.randint(1400, 2022)

    return year


def get_page_count() -> int:
    """
    Генерация случайного к-ва страниц
    :rtype: int
    :return: случайное количество страниц (от 1 до 1000)
    """

    page_count = random.randint(1, 1000)

    return page_count


def get_isbn() -> str:
    """
    Генерация случайного ISBN (Faker)
    :rtype: str
    :return: случайный ISBN
    """

    fake = Faker()
    isbn = fake.isbn13()

    return isbn


def get_rating() -> float:
    """
    Генерация случайной оценки (0-5 вкл. оба)
    :rtype: float
    :return: случайная средняя оценка (0-5)
    """

    rating = random.uniform(0, 5.0)
    rating = round(rating, 2)

    return rating


def get_price() -> float:
    """
    Генерация случайной цены
    :rtype: float
    :return: случайная цена (1-2000)
    """

    price = random.uniform(1.0, 2000.0)
    price = round(price, 2)

    return price


def get_discount() -> int:
    """
    Генерация случайной скидки
    :rtype: int
    :return: случайная скидка (от 1 до 99)
    """

    discount = random.randrange(1, 99)

    return discount


def get_author_list() -> list:
    """
    Генерация случайного списка авторов(1-3 автора, Faker)
    :rtype: list
    :return: список авторов размером от 1 до 3.
    """

    fake = Faker(locale="ru_RU")

    author_count = random.randrange(1, 4)

    author_list = [fake.name() for _ in range(author_count)]

    return author_list


def main() -> None:
    gen = dict_book_generator()

    json_list = [next(gen) for _ in range(100)]

    print(json_list)

    with open(JSON_PATHFILE, "w") as json_file:
        json.dump(json_list, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()