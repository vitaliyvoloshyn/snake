from __future__ import annotations

from snake.orm.models_ import Models, CharField, ForeignKey


def create_start_categories():
    start_categories = [
        ['Кулинарные курсы', 'img/kulinarnie_kursy.jpg', 'null'],
        ['Кондитерские курсы', 'img/konditerskie_kursi.jpg', 'null'],
        ['Мастер-классы', 'img/master-class.jpg', 'null']
    ]
    for el in start_categories:
        Category().objects.insert(*el)

def create_start_course_types():
    print('create types')
    types = ['online', 'record', 'live']
    for type_ in types:
        CourseType().objects.insert(type_)


class Category(Models):
    name = CharField()
    image = CharField()
    category_id = ForeignKey()


class CourseType(Models):
    name = CharField(60)


class Course(Models):
    name = CharField(max_length=60)
    category_id = ForeignKey(Category)
    coursetype_id = ForeignKey(CourseType)


class Student(Models):
    last_name = CharField(60, not_null=True)
    first_name = CharField(60)
    email = CharField(120, not_null=True, unique=True)
    phone = CharField(60)
    course_id = ForeignKey(Course)


queue_ = (Category, CourseType, Course, Student)

if __name__ == '__main__':
    print(Category().__dict__)
    print(Category().objects.filter(category_id='null'))
