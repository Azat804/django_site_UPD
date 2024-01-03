from django.urls import path 
from .views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('',FilmHome.as_view(), name='home'),
    path('post/<slug:post_slug>/',AddReview.as_view(), name='post'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/',LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('review/<str:user_str>/',ListReview.as_view(), name='review'),
    path('review/update/<slug:review_slug>/',UpdateReview.as_view(),name='update_review'),
    path('review/delete/<slug:review_slug>/',DeleteReview.as_view(),name='delete_review')
    #path('category/<int:cat_id>/',post, name='category')
]