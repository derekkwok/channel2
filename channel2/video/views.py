from channel2.base.views import ProtectedTemplateView


class IndexView(ProtectedTemplateView):

    template_name = 'video/index.html'

    def get(self, request):
        return self.render_to_response({})
