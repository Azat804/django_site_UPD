from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.

class FilmAdmin(admin.ModelAdmin):
    list_display=('id','slug','title', 'production_year','get_html_photo','director','film_duration','plot','rating',
                  'time_create','time_update','is_published') # список отображаемых полей в админ-панели
    list_display_links=('id','title') # список полей в виде ссылок для перехода к конкретной записи
    search_fields=('title','director') # поля, по которым можно производить поиск записей
    fieldsets = (
        ('Основные поля', {
            'fields': ('title','slug', 'production_year','photo', 'get_html_photo','director','plot','time_create','time_update'),# поля, которые отображаются в формах "добавить" и "изменить" 
        }),
        ('Расширенные настройки', {
            'classes': ('wide',),
            'fields': ('film_duration','is_published'),
        }),
    )
    list_editable=('is_published',) # редактируемые поля в списке записей в админ-панели
    list_filter=('title','director','production_year') # список полей для фильтрации записей в админ-панели
    prepopulated_fields={'slug':('title',)} # автоматически заполняет slug на основе поля title
    #fields=('title','slug','cat','content','photo','get_html_photo', 'is_published','time_create','time_update') # атрибут содержит порядок и список редактирумых полей
    readonly_fields=('time_create','time_update','get_html_photo') # нередактируемые поля
    save_on_top=True # кнопка сохранить появится и наверху

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100>")
        else:
            return "Нет фото"
    get_html_photo.short_description='Миниатюра'

class ReviewAdmin(admin.ModelAdmin):
    list_display=('id','user_name', 'comment','mark') # список отображаемых полей в админ-панели
    list_display_links=('id','user_name') # список полей в виде ссылок для перехода к конкретной записи
    search_fields=('user_name',) # поля, по которым можно производить поиск записей
    #prepopulated_fields={'slug':('user_name',)}

admin.site.register(Film, FilmAdmin) # регистрация моделей в админ-панели
admin.site.register(Review, ReviewAdmin)

admin.site.site_title = 'Админ-панель сайта о фильмах'
admin.site.site_header = 'Админ-панель сайта о фильмах'