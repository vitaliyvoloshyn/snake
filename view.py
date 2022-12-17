from datetime import datetime

from snake.views import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context(self) -> dict:
        context = {'cur_time': datetime.now().strftime('%Y.%m.%d %H:%M:%S')}
        return context


class DeveloperPageView(TemplateView):
    template_name = 'developer.html'
