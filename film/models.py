from django.db import models
from django.urls import reverse
# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length=255,unique=True, verbose_name='Заголовок') # verbose_name - альтернативное название полей в админ-панели
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    production_year = models.PositiveIntegerField(verbose_name='Год производства')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    director=models.CharField(max_length=255, verbose_name='Режиссер')
    film_duration=models.TimeField(verbose_name='Продолжительность фильма')
    plot=models.TextField(verbose_name='Сюжет')
    rating=models.FloatField(null=True,blank=True,verbose_name='Рейтинг')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self): # позволяет выводить поле title при чтение данных из БД (например, Film.objects.all())
        return self.title

    def get_absolute_url(self):
        return reverse('post',kwargs={'post_slug':self.slug})

    class Meta:
        verbose_name = 'Фильм' # название модели в админ-панели
        verbose_name_plural = 'Фильмы' # название модели в админ-панели во множественном числе
        ordering = ['-time_create', 'title'] # сортировка записей по двум полям в админ-панели и на сайте

class Review(models.Model):
    user_name= models.CharField(max_length=255, db_index=True, verbose_name='Имя пользователя')
    comment= models.TextField(max_length=1000,help_text = "Напишите свой отзыв",verbose_name='Рецензия')
    mark= models.PositiveSmallIntegerField(default=(5,'5'),choices = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],help_text = "Поставьте оценку",verbose_name='Оценка')
    film=models.ForeignKey('Film',on_delete=models.PROTECT, to_field='title', verbose_name='Фильм')

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse('update_review', kwargs={'review_slug': self.film.slug})

    class Meta:
        verbose_name = 'Рецензия' # название модели в админ-панели
        verbose_name_plural = 'Рецензии' # название модели в админ-панели во множественном числе
        ordering = ['user_name', 'film_id'] # сортировка записей по двум полям в админ-панели и на сайте
        unique_together = ['user_name', 'film_id']