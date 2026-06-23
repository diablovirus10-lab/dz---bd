import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    # homeworks = relationship("Homework", back_populates="courses")

    def __str__(self):
        return f'Course {self.id}: {self.name}'


class Homework(Base):
    __tablename__ = 'homeworks'

    id = sq.Column(sq.Integer, primary_key=True)
    number = sq.Column(sq.Integer, nullable=False)
    description = sq.Column(sq.Text, nullable=False)
    courses_id = sq.Column(sq.Integer, sq.ForeignKey('courses.id'), nullable=False)

    # course = relationship(Course, back_populates="homeworks")
    course = relationship(Course, backref='homeworks')

    def __str__(self):
        return f'Homework {self.id}: (номер: {self.number}), (описание: {self.description}), (связь с:{self.courses_id})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)