from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseNotFound
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .utils import *
from django.core.paginator import Paginator
from django.db.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

class FilmHome(DataMixin,ListView):
    model=Film
    template_name = 'film/index.html'
    context_object_name = 'posts' # название коллекции, куда помещаются данные из Film
    ordering='title'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Список фильмов')
        context=dict(list(context.items())+list(c_def.items()))
        return context

    def get_queryset(self):
        return Film.objects.filter(is_published=True)

#def index(request):
#    posts=Film.objects.all()
#    return render(request,'film/index.html',{'posts':posts})
# Create your views here.
class AddReview(DataMixin,CreateView):
    model=Review
    form_class = AddReviewForm
    template_name = 'film/post.html'
    slug_url_kwarg = 'post_slug' # переменная в url адресе
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post']=Film.objects.get(slug=self.kwargs['post_slug'])
        context['review']=Review.objects.filter(film__slug=self.kwargs['post_slug'])
        context['paginator']=Paginator(context['review'], per_page=3,orphans=1)
        page_number = self.request.GET.get('page')
        context['page_obj'] = context['paginator'].get_page(page_number)
        c_def=self.get_user_context(title=context['post'])
        
        context=dict(list(context.items())+list(c_def.items()))
        print(context)
        return context

    def form_valid(self,form): # метод вызывается при правильном заполнении формы
        if  Review.objects.filter(user_name=self.request.user.username, film__slug=self.kwargs['post_slug']).exists():
            form.add_error(None, 'Вы уже написали рецензию к данному фильму')
            response = super().form_invalid(form)
            return response
        else:
            f=form.save(commit=False)
            f.user_name=self.request.user.username
            f.film_id=self.get_context_data()['post']
            f.save()
            avg=Review.objects.filter(film__slug=self.kwargs['post_slug']).aggregate(avg=Avg('mark'))['avg']
            Film.objects.filter(slug=self.kwargs['post_slug']).update(rating=avg)
            return redirect('home')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'film/register.html'
    success_url = reverse_lazy('home')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    authentication_form = LoginUserForm
    template_name = 'film/login.html'
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

def logout_user(request):
    logout(request)
    return redirect('login')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'film/contact.html'
    success_url = reverse_lazy('home')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))
 
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

def post(request,post_slug):
    post=Film.objects.get(slug=post_slug)
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                params=form.cleaned_data
                params['film_id']=post.title
                params['user_name']=post_slug
                params['mark']=int(params['mark'])
                #print(params)
                #Review.objects.create(**params)
                #form.fields['film_id']=post.title
                #form.fields['user_name']=post_slug
                f=form.save(commit=False)
                f.user_name=post_slug
                f.film_id=post.title
                f.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddReviewForm()
    context={'post':post, 'form':form}
    return render(request,'film/post.html',context=context)


class ListReview(DataMixin,ListView):
    model=Review
    template_name = 'film/review.html'
    context_object_name = 'reviews' # название коллекции, куда помещаются данные из Film
    ordering='film_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Мои рецензии')
        context=dict(list(context.items())+list(c_def.items()))
        return context

    def get_queryset(self):
        return Review.objects.filter(user_name=self.request.user.username)


class UpdateReview(DataMixin,UpdateView):
    model=Review
    #queryset=Review.objects.get(pk=1)
    query_pk_and_slug=True
    form_class = AddReviewForm
    template_name = 'film/update.html'
    slug_url_kwarg = 'review_slug' # переменная в url адресе
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post']=Film.objects.get(slug=self.kwargs['review_slug'])
        #context['review']=Review.objects.filter(film__slug=self.kwargs['review_slug'])
        c_def=self.get_user_context(title=context['post'])
        context=dict(list(context.items())+list(c_def.items()))
        return context

    def get_object(self):
        return Review.objects.get(user_name=self.request.user.username, film__slug=self.kwargs['review_slug'])

    def form_valid(self,form): # метод вызывается при правильном заполнении формы
            f=form.save(commit=False)
            f.user_name=self.request.user.username
            f.film_id=self.get_context_data()['post']
            f.save()
            avg=Review.objects.filter(film__slug=self.kwargs['review_slug']).aggregate(avg=Avg('mark'))['avg']
            Film.objects.filter(slug=self.kwargs['review_slug']).update(rating=avg)
            return redirect('home')


class DeleteReview(DataMixin,DeleteView):
    model=Review
    #queryset=Review.objects.get(pk=1)
    query_pk_and_slug=True
    form_class = AddReviewForm
    template_name = 'film/delete.html'
    slug_url_kwarg = 'review_slug' # переменная в url адресе
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post']=Film.objects.get(slug=self.kwargs['review_slug'])
        #context['review']=Review.objects.filter(film__slug=self.kwargs['review_slug'])
        c_def=self.get_user_context(title=context['post'])
        context=dict(list(context.items())+list(c_def.items()))
        return context

    def get_object(self):
        return Review.objects.get(user_name=self.request.user.username, film__slug=self.kwargs['review_slug'])

    def form_valid(self,form): # метод вызывается при правильном заполнении формы
            #f=form.save(commit=False)
            #f.user_name=self.request.user.username
            #f.film_id=self.get_context_data()['post']
            #f.save()
            form.delete()
            avg=Review.objects.filter(film__slug=self.kwargs['review_slug']).aggregate(avg=Avg('mark'))['avg']
            Film.objects.filter(slug=self.kwargs['review_slug']).update(rating=avg)
            return reverse_lazy('home')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
