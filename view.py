from datetime import datetime

from patterns.creational_patterns import Engine, Category
from snake.request import Request
from snake.response import Response, ResponseHTML
from snake.views import TemplateView

site = Engine()


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context(self) -> dict:
        context = {'cur_time': datetime.now().strftime('%Y.%m.%d %H:%M:%S')}
        return context


class LearnCookPageView(TemplateView):
    template_name = 'learn_cooking.html'

    def get_context(self) -> dict:
        context = {'category': site.categories}
        return context


class DetailCategoryView(TemplateView):
    template_name = 'detail_category.html'

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        id_ = request.GET.get('id')
        if id_ is None:
            raise Exception('Не указан id категории')
        object = site.find_category_by_id(int(id_[0]))
        context = self.get_context(object)
        return ResponseHTML(status_code=self.status_code, template_name=self.template_name, context=context)

    def get_context(self, category: Category) -> dict:
        return {'object': category}


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
