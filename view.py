from datetime import datetime

from snake.request import Request
from snake.response import Response
from snake.views import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context(self) -> dict:
        context = {'cur_time': datetime.now().strftime('%Y.%m.%d %H:%M:%S')}
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
