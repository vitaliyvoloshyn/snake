from datetime import datetime
from typing import List, Union

from patterns.patterns import Engine, CoursesTypes, Course, Category
from patterns.structural_patterns import AppRout, debug
from snake.request import Request
from snake.response import Response
from snake.views import TemplateView

site = Engine()


@AppRout('')
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context(self) -> dict:
        context = super().get_context()
        context['cur_time'] = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        return context


@AppRout('/learncook')
class LearnCookPageView(TemplateView):
    template_name = 'learn_cooking.html'

    def get_context(self) -> dict:
        context = super().get_context()
        context['category'] = site.get_categories()
        return context

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        cat = request.POST.get('category')[0]
        site.create_category(name=cat)
        return super().post(request)


@AppRout('/learncook/category')
class DetailCategoryView(TemplateView):
    template_name = 'detail_category.html'

    @debug
    def get(self, request: Request = None, *args, **kwargs) -> Response:
        self.parent_category = self._get_parent_category(request.GET.get('name')[0])
        if self.parent_category is None:
            raise Exception('Не указано имя категории')
        self.context = self.get_context()
        return super().get(request)

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        operation = request.POST.get('operation')[0]
        self.parent_category = self._get_parent_category(request.POST.get('parent_category')[0])
        if operation == 'add_subcategory':
            new_category = request.POST.get('subcategory_name')[0]
            site.create_category(name=new_category, parent_category=self.parent_category)
        elif operation == 'add_course':
            new_course = request.POST.get('course_name')[0]
            course_type = getattr(CoursesTypes, request.POST.get('course_type')[0])
            site.create_course(type_=course_type, name=new_course, parent_category=self.parent_category)

        elif operation == 'clone_course':
            new_course = site.get_component_by_name(request.POST.get('course_name')[0])
            site.clone_course(new_course)
        return super().post(request)

    @staticmethod
    def _get_parent_category(category_name: str) -> Category:
        return site.get_component_by_name(category_name)

    def get_context(self) -> dict:
        context = super().get_context()
        context['category'] = self.parent_category
        context['subcategories'] = self._get_child_categories(self.parent_category)
        context['courses'] = self._get_child_courses(self.parent_category)
        context['courses_types'] = list(CoursesTypes().__dict__.keys())
        return context

    @staticmethod
    def _get_child_categories(parent_category: Category) -> List[Union[Category, None]]:
        child_categories = list(filter(lambda x: isinstance(x, Category), parent_category.children))
        return child_categories

    @staticmethod
    def _get_child_courses(parent_category: Category) -> List[Union[Course, None]]:
        child_courses = list(filter(lambda x: isinstance(x, Course), parent_category.children))
        return child_courses


@AppRout('/developer')
class DeveloperPageView(TemplateView):
    template_name = 'developer.html'


@AppRout('/about')
class AboutPageView(TemplateView):
    template_name = 'about.html'


@AppRout('/firstgallery')
class FirstGalleryPageView(TemplateView):
    template_name = 'first_gallery.html'


@AppRout('/secondgallery')
class SecondGalleryPageView(TemplateView):
    template_name = 'second_gallery.html'


@AppRout('/thirdgallery')
class ThirdGalleryPageView(TemplateView):
    template_name = 'third_gallery.html'


@AppRout('/contact')
class ContactPageView(TemplateView):
    template_name = 'contact.html'

    @debug
    def post(self, request: Request = None, *args, **kwargs) -> Response:
        contact_name = request.POST.get('contact_name')[0]
        contact_mail = request.POST.get('contact_email')[0]
        contact_message = request.POST.get('contact_message')[0]
        self._write_to_file_contact_message(contact_name, contact_mail, contact_message)
        return super().post()

    @staticmethod
    def _write_to_file_contact_message(name: str, email: str, message: str):
        filename = 'contact message.txt'
        out_str = f'{name}, {email}, {message}\n'
        print(out_str)
        with open(filename, 'a', encoding='windows-1251') as f:
            f.write(out_str)
