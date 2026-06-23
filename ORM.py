import sqlalchemy
from sqlalchemy.orm import sessionmaker

from model_ORM import *

DSN = 'postgresql://postgres:Er63mk1xc@localhost:5432/test'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

course1 = Course(name='Python')

session.add(course1)
session.commit()

print(course1)

hw1 = Homework(number=1, description='простая дз', course=course1)
hw2 = Homework(number=2, description='сложная дз', course=course1)
session.add_all([hw1, hw2])
session.commit()

for c in session.query(Homework).filter(Homework.number == 1).all():
    print(c)
for c in session.query(Homework).filter(Homework.description.like('%сложн%')).all():
    print(c)

for c in session.query(Course).join(Homework.course).filter(Homework.number == 2).all():
    print(c)

course2 = Course(name='java')
session.add(course2)
session.commit()

subq = session.query(Homework).filter(Homework.description.like('%сложн%')).subquery()
for c in session.query(Course).join(subq, Course.id == subq.c.courses_id).all():
    print(c)

session.query(Course).filter(Course.name == 'java').update({'name':'java_script'})
session.commit()

session.query(Course).filter(Course.name == 'java_script').delete()
session.commit()

session.close()