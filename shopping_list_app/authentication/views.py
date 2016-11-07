from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect, render
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View


# class LoginView(View):
#     '''Handles Login'''
#     def get(self, request):
#         form = AuthenticationForm()

#         context = {}
#         context.update(csrf(request))
#         context.update({'form': form})
#         return render(request, 'authentication/login.html', context)

#     def post(self, request):
#         form = AuthenticationForm(data=request.POST)

#         if form.is_valid():
#             login(request, form.get_user())
#             return HttpResponseRedirect(reverse('index'))

#         else:
#             for key in form.errors:
#                 for error in form.errors[key]:
#                     messages.add_message(request, messages.INFO, error)

#             context = {}
#             context.update(csrf(request))
#             context.update({'form': form})
#             return render(request, 'authentication/login.html', context)


class LoginView(FormView):
    '''Handles Login'''
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'authentication/login.html'

    def form_valid(self, form):
        '''Login user if form is valid'''
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
