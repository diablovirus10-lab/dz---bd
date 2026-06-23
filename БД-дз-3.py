import json

import os
from dotenv import load_dotenv

import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from model_ORM_2 import *



load_dotenv()

User = os.getenv("USER")
Password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
name_BD = os.getenv("NAME_BD2")

DSN = f"postgresql://{User}:{Password}@{host}:{port}/{name_BD}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)


def code(session, json_load):
    def t(s):
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return f"{dt:%Y-%m-%d %H:%M:%S}.{dt:%f}"[:-3]

    for j in json_load:
        if j["model"] == "publisher":
            pub = j.get("fields").get("name")
            model_pub = Publisher(name=pub)
            session.add(model_pub)
            session.flush()

        elif j["model"] == "book":
            book = j.get("fields").get("title")
            id_pub_book = j.get("fields").get("id_publisher")
            model_book = Book(title=book, id_publisher=id_pub_book)
            session.add(model_book)
            session.flush()

        elif j["model"] == "shop":
            shop = j.get("fields").get("name")
            model_shop = Shop(name=shop)
            session.add(model_shop)
            session.flush()

        elif j["model"] == "stock":
            id_stock_book = j.get("fields").get("id_book")
            id_stock_shop = j.get("fields").get("id_shop")
            stock_count = j.get("fields").get("count")
            model_stock = Stock(id_book=id_stock_book, id_shop=id_stock_shop, count=stock_count)
            session.add(model_stock)
            session.flush()

        elif j["model"] == "sale":
            price_sale = j.get("fields").get("price")
            date_sale_stock = j.get("fields").get("date_sale")
            id_stock_sale = j.get("fields").get("id_stock")
            sale_count = j.get("fields").get("count")
            model_sale = Sales(price=price_sale, date_sale=t(date_sale_stock), id_stock=id_stock_sale, count=sale_count)
            session.add(model_sale)
            session.commit()


def sales_publisher(session, publisher_query):
    q = (
        session.query(
            Book.title.label("book_name"),
            Shop.name.label("shop_name"),
            Sales.price,
            Sales.date_sale
        )
        .join(Stock, Sales.stock)
        .join(Book, Stock.book)
        .join(Publisher, Book.publisher)
        .join(Shop, Stock.shop)
    )

    try:
        pub_id = int(publisher_query)
        q = q.filter(Publisher.id == pub_id)
    except ValueError:
        q = q.filter(Publisher.name.ilike(f"%{publisher_query}%"))

    q = q.order_by(Sales.date_sale.desc())

    rows = q.all()
    if not rows:
        print("Нету")
        return

    print()
    for row in rows:
        date_str = row.date_sale.strftime("%Y-%m-%d")
        price_str = (
            f"{row.price:.2f}".rstrip(".").rstrip("0")
            if row.price == int(row.price)
            else f"{row.price:2f}"
        )
        print(f"{row.book_name:<50} | {row.shop_name:<30} | {price_str:<10} | {date_str:<10}")


def load_json_file(filename="tests_data.json"):
    papka = "test_danni"
    with open(f"{papka}/{filename}", "r", encoding="utf-8") as f:
        loaded_json = json.load(f)
    return loaded_json


def main():
    session = Session()
    json_load = load_json_file()
    try:
        code(session, json_load)

        print("Доступные авторы:\n")
        for p in session.query(Publisher).all():
            print(f"\t[{p.id}]: {p.name}")
        publisher_input = input("\nВыберите автора:")
        if not publisher_input:
            return

        sales_publisher(session, publisher_input)
    finally:
        session.close()

if __name__ == "__main__":
    main()