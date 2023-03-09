from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView

from .models import *
from .forms import *
from .utils import *


# Create your views here.
class ArtistsHome(DataMixin, ListView):
    model = Artists
    template_name = "artists/index.html"
    context_object_name = "posts"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Artists.objects.filter(is_published=True).select_related("cat")


def about(request):
    contact_list = Artists.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "artists/about.html", {"menu": menu, "page_obj": page_obj, "title": "О сайте"})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")

# Если не указывать success_url django перекинет на только что
# созданную страницу
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "artists/addpage.html"
    success_url = reverse_lazy("home")
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "artists/contact.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
# def contact(request):
    # return HttpResponse("Обратная связь")
# 
# def login(request):
#     return HttpResponse("Авторизация")



class ShowPost(DataMixin, DetailView):
    model = Artists
    template_name = "artists/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))



class ArtistsCategory(DataMixin, ListView):
    model = Artists
    template_name = "artists/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Artists.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(title="Категория - " + c.name, 
                                            cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "artists/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "artists/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')