from django.apps import AppConfig


class FilmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'film'
    verbose_name = 'Фильмы' # название приложения в админ-панели
