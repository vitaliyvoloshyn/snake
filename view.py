from datetime import datetime

from patterns.creational_patterns import Engine, Category, CoursesTypes, get_logger
from snake.request import Request
from snake.response import Response, ResponseHTML
from snake.views import TemplateView

site = Engine()


class HomePageView(TemplateView):
    template_name = 'index.html'
    def get_context(self) -> dict:
        context = super(HomePageView, self).get_context()
        context['cur_time'] = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        return context


class LearnCookPageView(TemplateView):
    template_name = 'learn_cooking.html'

    def get_context(self) -> dict:
        context = super().get_context()
        context['category'] = site.categories
        return context

    def post(self, request: Request = None, *args, **kwargs) -> Response:
        cat = request.POST.get('category')[0]
        site.create_category(name=cat)
        return super(LearnCookPageView, self).post(request)


class DetailCategoryView(TemplateView):
    template_name = 'detail_category.html'

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        self.category_id = int(request.GET.get('id')[0])
        if self.category_id is None:
            raise Exception('Не указан id категории')
        self.context = self.get_context()
        return super().get(request)

    def post(self, request: Request = None, *args, **kwargs) -> Response:

        operation = request.POST.get('operation')[0]
        self.category_id = int(request.POST.get('category_id')[0])
        category = site.find_category_by_id(self.category_id)
        course_name = request.POST.get('course_name')[0]
        self.context = self.get_context()
        if operation == 'create_course':
            course_type = request.POST.get('course_type')[0]
            category.create_course(getattr(CoursesTypes, course_type), course_name)

        elif operation == 'clone_course':
            category.clone_course(course_name)
        return super().post(request)



    def get_context(self) -> dict:
        context = super().get_context()
        context['category'] = site.find_category_by_id(self.category_id)
        context['courses_types'] = list(CoursesTypes().__dict__.keys())
        return context


class DeveloperPageView(TemplateView):
    template_name = 'developer.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class FirstGalleryPageView(TemplateView):
    template_name = 'first_gallery.html'


class SecondGalleryPageView(TemplateView):
    template_name = 'second_gallery.html'


class ThirdGalleryPageView(TemplateView):
    template_name = 'third_gallery.html'


class ContactPageView(TemplateView):
    template_name = 'contact.html'

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
