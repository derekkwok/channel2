from channel2.base.views import TemplateView


class IndexView(TemplateView):

    template_name = 'video/index.html'

    def get(self, request):
        return self.render_to_response({})
