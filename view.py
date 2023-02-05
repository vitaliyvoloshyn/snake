from datetime import datetime
from sqlite3 import IntegrityError

from models import Category, Course, CourseType, Student
from patterns.patterns import EmailNotifier, PhoneNotifier
from patterns.structural_patterns import AppRout, debug
from snake.orm.exception import RecordNotFoundException
from snake.request import Request
from snake.response import Response, ResponceRedirect
from snake.views import TemplateView, ListView, DetailView


def create_category(name: str, image: str, parent_category: int) -> None:
    """Создание новой категории"""
    parent_category = parent_category if parent_category else 'null'
    Category().objects.insert(name, image, parent_category)


@AppRout('')
class HomePageView(TemplateView):
    """Домашняя страница"""
    template_name = 'index.html'

    def get_context(self) -> dict:
        context = super().get_context()
        context['cur_time'] = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        return context


@AppRout('/learncook')
class LearnCookPageView(TemplateView):
    """Страница обучения"""
    template_name = 'learn_cooking.html'

    def get_context(self) -> dict:
        context = super().get_context()
        lst = []
        for cat in Category().objects.filter(category_id='null'):
            dct = {}
            dct['name'] = cat.name
            dct['id'] = cat.categoryId
            dct['path_img'] = cat.image
            dct['subcategories'] = len(Category().objects.filter(category_id=cat.categoryId))
            dct['courses'] = len(Course().objects.filter(category_id=cat.categoryId))
            lst.append(dct)

        context['category'] = lst
        return context

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        cat = request.POST.get('category')[0]
        image = request.POST.get('image')[0]
        parent_category = int(request.POST.get('parent', 0)[0])
        create_category(cat, image, parent_category)
        return ResponceRedirect(to='/learncook', )


@AppRout('/learncook/category')
class DetailCategoryView(TemplateView):
    """Страница категории"""
    template_name = 'detail_category.html'

    @debug
    def get(self, request: Request = None, *args, **kwargs) -> Response:
        try:
            category_id = request.GET.get('id', None)[0]
            self.category = Category().objects.find_by_id(category_id)
        except (RecordNotFoundException, TypeError):
            return Response('404 NOT FOUND', body=b'404 NOT FOUND')
        self.context = self.get_context()
        return super().get(request)

    @staticmethod
    def subcategories_count(category_id):
        return len(Category().objects.filter(category_id=category_id))

    @staticmethod
    def courses_count(category_id):
        return len(Course().objects.filter(category_id=category_id))

    @staticmethod
    def get_course_type(course_id):
        return CourseType().objects.find_by_id(course_id)

    def get_context(self) -> dict:
        context = super().get_context()
        context['category'] = self.category
        context['subcategories'] = Category().objects.filter(category_id=self.category.categoryId)
        context['subcategories_count'] = self.subcategories_count
        context['courses_count'] = self.courses_count
        context['courses'] = Course().objects.filter(category_id=self.category.categoryId)
        context['courses_types'] = CourseType().objects.all()
        context['course_type'] = self.get_course_type
        return context


    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        operation = request.POST.get('operation')[0]
        parent_id = request.POST.get('parent_category')[0]
        if operation == 'add_subcategory':
            new_category = request.POST.get('subcategory_name')[0]
            image = request.POST.get('image')[0]
            create_category(name=new_category, image=image, parent_category=parent_id)
        elif operation == 'add_course' or operation == 'clone_course':
            new_course = request.POST.get('course_name')[0]
            type_ = request.POST.get('course_type')[0]
            Course().objects.insert(new_course, parent_id, type_)
        elif operation == 'notify':
            course_id = request.POST.get('course_id')[0]
            for student in Student().objects.filter(course_id=course_id):
                EmailNotifier.notify(student)
                PhoneNotifier.notify(student)
        query = request.GET.get('raw_query_string')
        return ResponceRedirect(to=f'/learncook/category?{query}')

@AppRout('/developer')
class DeveloperPageView(TemplateView):
    """Страница о разработчике"""
    template_name = 'developer.html'


@AppRout('/about')
class AboutPageView(TemplateView):
    """Страница о сайте"""
    template_name = 'about.html'


@AppRout('/firstgallery')
class FirstGalleryPageView(TemplateView):
    """Страница первой галереи"""
    template_name = 'first_gallery.html'


@AppRout('/secondgallery')
class SecondGalleryPageView(TemplateView):
    """Страница второй галереи"""
    template_name = 'second_gallery.html'


@AppRout('/thirdgallery')
class ThirdGalleryPageView(TemplateView):
    """Страница третьей галереи"""
    template_name = 'third_gallery.html'


@AppRout('/contact')
class ContactPageView(TemplateView):
    """Страница обратной связи"""
    template_name = 'contact.html'

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        contact_name = request.POST.get('contact_name')[0]
        contact_mail = request.POST.get('contact_email')[0]
        contact_message = request.POST.get('contact_message')[0]
        self._write_to_file_contact_message(contact_name, contact_mail, contact_message)
        return ResponceRedirect(to='/contact')

    @staticmethod
    def _write_to_file_contact_message(name: str, email: str, message: str):
        filename = 'contact message.txt'
        out_str = f'{name}, {email}, {message}\n'
        print(out_str)
        with open(filename, 'a', encoding='windows-1251') as f:
            f.write(out_str)


@AppRout('/registration')
class Registration(TemplateView):
    """Страница регистрации"""
    template_name = 'registration.html'

    def get_context(self) -> dict:
        context = super().get_context()
        context['courses'] = Course().objects.all()
        return context

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        try:
            self._create_student(request)
            return ResponceRedirect(to='/successful_registration')
        except IntegrityError as err:
            error_message = 'This email address is already registered'
            return ResponceRedirect(to=f'/error_registration?message={error_message}')

    @staticmethod
    def _create_student(request: Request):
        f_n = request.POST.get('first_name')[0]
        l_n = request.POST.get('last_name')[0]
        email = request.POST.get('email')[0]
        phone = request.POST.get('phone')[0]
        course = request.POST.get('course')[0]
        Student().objects.insert(f_n, l_n, email, phone, course)


@AppRout('/successful_registration')
class SuccessfullRegistration(TemplateView):
    """Страница успешной регистрации"""
    template_name = 'successfull_registration.html'

error_message = ''

@AppRout('/error_registration')
class ErrorRegistration(TemplateView):
    """Страница неудачной регистрации"""
    template_name = 'error_registration.html'
    context = {'message': error_message}

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        self.message = request.GET.get('message')[0]
        return super().get(request, *args, **kwargs)

    def get_context(self) -> dict:
        return {'message': self.message}



@AppRout('/students_list')
class StudentsLstView(ListView):
    """Страница со списком студентов"""
    template_name = 'students_list.html'
    model = Student


@AppRout('/student')
class DetailStudentView(DetailView):
    """Страница студента"""
    template_name = 'detail_student.html'
    model = Student

    def get_context(self) -> dict:
        context = super().get_context()
        course = self._get_course(context[self.context_object_name].course_id)
        context['course'] = course
        print(context)

        return context

    def _get_course(self, course_id: int):
        print(course_id)
        return Course().objects.find_by_id(course_id)

