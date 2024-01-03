from .models import *

menu = [
        {'title': "Главная страница", 'url_name':'home'}, {'title': "Обратная связь", 'url_name': 'contact'}
        
]
class DataMixin:
    paginate_by = 2
    paginate_orphans=1

    def get_user_context(self, **kwargs):
        context = kwargs
        #cats = Category.objects.all()
       
        
        context['menu'] = menu
        #context['cats'] = cats
        #if 'cat_selected' not in context:
        #    context['cat_selected'] = 0
        return context