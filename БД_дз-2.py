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
name_BD = os.getenv("NAME_BD")

DSN = f"postgresql://{User}:{Password}@{host}:{port}/{name_BD}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)

def code(session):

    pushkin = Publisher(name="Пушкин")
    dostoevsky = Publisher(name="Достоевский")

    session.add_all([pushkin, dostoevsky])
    session.flush()


    books = [
        Book(title="Руслан и Людмила", id_publisher=pushkin.id),
        Book(title="Кавказский пленник", publisher=pushkin),
        Book(title="Медный всадник", publisher=pushkin),
        Book(title="Полтава", publisher=pushkin),
        Book(title="Дубровский", publisher=pushkin),
        Book(title="Пиковая дама", publisher=pushkin),
        Book(title="Капитанская дочка", publisher=pushkin),
        Book(title="Борис Годунов", publisher=pushkin),
        Book(title="Бедные люди", publisher=dostoevsky),
        Book(title="Униженные и оскорбленные", publisher=dostoevsky),
        Book(title="Преступление и наказание", publisher=dostoevsky),
        Book(title="Игрок", publisher=dostoevsky),
        Book(title="Идиот", publisher=dostoevsky),
        Book(title="Бесы", publisher=dostoevsky),
        Book(title="Подросток", publisher=dostoevsky),
        Book(title="Братья Карамазовы", publisher=dostoevsky)
    ]

    session.add_all(books)
    session.flush()


    literary_haven = Shop(name="Литературный рай")
    wordsmith = Shop(name="Невидимка")

    session.add_all([literary_haven, wordsmith])
    session.flush()


    stocks = [
        Stock(book=books[0], shop=literary_haven, count=100),
        Stock(book=books[1], shop=literary_haven, count=100),
        Stock(book=books[2], shop=literary_haven, count=100),
        Stock(book=books[3], shop=literary_haven, count=100),
        Stock(book=books[4], shop=literary_haven, count=100),
        Stock(book=books[5], shop=wordsmith, count=100),
        Stock(book=books[6], shop=wordsmith, count=100),
        Stock(book=books[7], shop=wordsmith, count=100),
        Stock(book=books[8], shop=literary_haven, count=150),
        Stock(book=books[9], shop=literary_haven, count=150),
        Stock(book=books[10], shop=literary_haven, count=150),
        Stock(book=books[11], shop=wordsmith, count=150),
        Stock(book=books[12], shop=wordsmith, count=150),
        Stock(book=books[13], shop=wordsmith, count=150),
        Stock(book=books[14], shop=wordsmith, count=150),
        Stock(book=books[15], shop=wordsmith, count=150)
    ]

    session.add_all(stocks)
    session.flush()


    def d(s): return datetime.strptime(s, "%d-%m-%Y").date()
    sales = [
        Sales(price=500, date_sale=d("09-11-2022"), stock=stocks[0], count=40),
        Sales(price=600, date_sale=d("07-10-2021"), stock=stocks[1], count=40),
        Sales(price=500, date_sale=d("15-8-2020"), stock=stocks[2], count=40),
        Sales(price=400, date_sale=d("20-9-2020"), stock=stocks[3], count=40),
        Sales(price=350, date_sale=d("30-12-2021"), stock=stocks[4], count=40),
        Sales(price=700, date_sale=d("15-7-2019"), stock=stocks[5], count=40),
        Sales(price=650, date_sale=d("14-1-2021"), stock=stocks[6], count=40),
        Sales(price=400, date_sale=d("16-8-2021"), stock=stocks[7], count=40),
        Sales(price=700, date_sale=d("18-10-2020"), stock=stocks[8], count=40),
        Sales(price=650, date_sale=d("25-2-2023"), stock=stocks[9], count=40),
        Sales(price=450, date_sale=d("11-9-2024"), stock=stocks[10], count=40),
        Sales(price=380, date_sale=d("18-12-2021"), stock=stocks[11], count=40),
        Sales(price=670, date_sale=d("12-8-2025"), stock=stocks[12], count=40),
        Sales(price=480, date_sale=d("19-8-2023"), stock=stocks[13], count=40),
        Sales(price=570, date_sale=d("29-11-2021"), stock=stocks[14], count=40),
        Sales(price=800, date_sale=d("06-12-2024"), stock=stocks[15], count=40)
    ]

    session.add_all(sales)
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
        print(f"По запросу '{publisher_query}' продаж не найдено")
        return

    print()
    for row in rows:
        date_str = row.date_sale.strftime("%d-%m-%Y")
        price_str = (
            f"{row.price:.2f}".rstrip("0").rstrip(".")
            if row.price == int(row.price)
            else f"{row.price:.2f}"
        )
        print(f"{row.book_name:<30} | {row.shop_name:<30} | {price_str:<10} | {date_str:<10}")




def main():
    session = Session()
    try:
        code(session)

        print("Доступные издатели:")
        for p in session.query(Publisher).all():
            print(f"\t[{p.id}]: {p.name}")

        publisher_input = input("\nВыберите автора:")
        if not publisher_input:
            print("Ввод пустой")
            return

        sales_publisher(session, publisher_input)
    finally:
        session.close()


if __name__ == '__main__':
    main()