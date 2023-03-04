from django.urls import path
from . import views
from authentication.views import login_view
urlpatterns = [

    path('', views.index),
    path("search/", views.search, name="search"),
    path("tv/<int:tv_id>/", views.view_tv_detail, name="tvdetail"),
    path("movie/<int:movie_id>/", views.view_movie_detail, name="moviedetail"),
    path("api/trendings/", views.view_trendings_results, name="trendings"),
    path("movie/<int:movie_id>/comments/", views.comment_page, name="comments"),

]