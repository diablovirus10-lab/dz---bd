import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'Publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), nullable=False, unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Book(Base):
    __tablename__ = 'Book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False, unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('Publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='Book')

    def __str__(self):
        return f"{self.title} ({self.publisher})"


class Shop(Base):
    __tablename__ = 'Shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Stock(Base):
    __tablename__ = 'Stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('Book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='Stock')
    shop = relationship(Shop, backref='Stock')

    def __str__(self):
        return f"{self.id}: {self.book}, кол-во: {self.count} ({self.shop})"


class Sales(Base):
    __tablename__ = 'Sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(10, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='Sale')

    def __str__(self):
        return f"Товар {self.id}: {self.price}, кол-во: {self.count}, дата: {self.date_sale}"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
