from django.contrib.auth import logout, login
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.base import View

from channel2.account.forms import LoginForm
from channel2.base.views import TemplateView


class LoginView(TemplateView):

    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_to_response({'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next', reverse('index')))
        return self.render_to_response({'form': form})


class LogoutView(View):

    def get(self, request):
        return HttpResponseNotAllowed(permitted_methods=['post'])

    def post(self, request):
        logout(request)
        return redirect('account:login')
