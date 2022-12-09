from datetime import datetime

from snake.views import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context(self) -> dict:
        context = {'current_time': datetime.now().strftime('%Y.%m.%d %H:%M:%S'),
                   'name': 'Ваше Величество'}
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'
