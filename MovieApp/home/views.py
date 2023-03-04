from django.shortcuts import render, redirect
import requests
from django.http.response import JsonResponse
from .models import Comment
from django.contrib.auth.models import User

from django.http import HttpResponse


TMDB_API_KEY = "973911d6291b5a466f7f0f47614d960e"

# Create your views here.
def search(request):

    # get the query from the searxh box
    query = request.GET.get('q')
    print(query)

    # if the query is not empty
    results = []
    if query:

        data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")          
        print(data.json())
    else:
        return HttpResponse("please enter a search query")
    
    
    return render(request, 'home/results.html', {
        "data": data.json(),
        "type": request.GET.get("type")
        })


def index(request):
    return render(request, 'home/index.html')      



def view_tv_detail(request, tv_id):
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")

    return render(request, "home/tv_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "tv",

    }
    )

def view_movie_detail(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")    
    recommendations = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
   

    return render(request, "home/movie_detail.html", {
        "data":data.json(),
        "recommendations": recommendations.json(),
        "type": "movie",

    })


def view_trendings_results(request):
    type = request.GET.get("media_type")
    time_window = request.GET.get("time_window")

    trendings = requests.get(f"https://api.themoviedb.org/3/trending/{type}/{time_window}?api_key={TMDB_API_KEY}&language=en-US")
    return JsonResponse(trendings.json())

def comment_page(request, movie_id):
    if request.method == "POST":
       user = request.user
       comment = request.POST.get("comment")

       if not request.user.is_authenticated:
        user = User.objects.get(id=1)


       Comment(comment=comment, user=user, movie_id=movie_id).save()
       return redirect(f"/movie/{movie_id}/comments/")
    else:
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
        title = data.json()["title"]

        comments = Comment.objects.filter(movie_id=movie_id)



        return render(request, "home/comments.html" , {
            "title": title,
            "comments": comments,
        })