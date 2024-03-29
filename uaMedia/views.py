
from django.views.generic.base import View
from django.views.generic import ListView,DetailView

from django.http import JsonResponse
from .models import Movie, Category, Actor, Genre, Rating
from django.shortcuts import redirect
# Create your views here.
from django.db.models import Q, Sum, Max, Min, Count, Avg, Value
from http.client import HTTPResponse
from .forms import ReviewForm, RatingForm


class GenreYear:

  def get_genres(self):
    return Genre.objects.all()

  def get_years(self):
    return Movie.objects.filter(draft=False).values('year')


class MovieView(GenreYear, ListView):
  """ Список всех фильмов"""
  model = Movie
  queryset = Movie.objects.filter(draft=False)
  #template_name = "uaMedia/movies.html"
  paginate_by = 2



class MovieDetailView(GenreYear,DetailView):
  """ Полное описание фильма """
  model = Movie
  slug_field ="url"
  movie = Movie.objects.all()
  agg = movie.aggregate(Min('year'))

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)        
    context['star_form'] = RatingForm()
    context['agg'] = self.agg
    return context

class AddReview(View):
  """ Отзывы"""
  def post(self,request, pk):
    form = ReviewForm(request.POST)
    movie = Movie.objects.get(id=pk)
    if form.is_valid():
      form = form.save(commit=False)
      form.movie = movie
      if request.POST.get('parent', None):
        form.parent_id = int(request.POST.get('parent'))
         
      form.save()
    return redirect(movie.get_absolute_url())


class ActorView(GenreYear,DetailView):
  """Вывод информации о актере"""
  model = Actor
  template_name = 'uaMedia/actor.html'
  slug_field = "name"
  


class FilterMoviesView(GenreYear, ListView):
  paginate_by = 2
  """Фильтр фильмов"""
  def get_queryset(self) :
    queryset = Movie.objects.filter(Q(
      year__in=self.request.GET.getlist("year")) | Q(genres__in= self.request.GET.getlist("genre")
    )).distinct()
    return queryset

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['year']  = ''.join([f"year={x}&" for x in self.request.POST.getlist("year")])
    context['genre']  = ''.join([f"genre={x}&" for x in self.request.POST.getlist("genre")])
    return context
    
class JsonFilterMoviesView(ListView):
  """Фильтр фильмов в json"""
  def get_queryset(self):
      queryset = Movie.objects.filter(
          Q(year__in=self.request.GET.getlist("year")) |
          Q(genres__in=self.request.GET.getlist("genre"))
      ).distinct().values("title", "tagline", "url", "poster")
      return queryset

  def get(self, request, *args, **kwargs):
      queryset = list(self.get_queryset())
      return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
  """ Добавление рейтинга фильму"""
  def get_client_ip(self,request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
    else:
      ip = request.META.get('REMOTE_ADDR')
    return ip


  def post(self,request):
    form = RatingForm(request.POST)
    if form.is_valid():
      Rating.objects.update_or_create(
        ip= self.get_client_ip(request),
        movie_id=int(request.POST.get("movie")),
        defaults={'star_id' : int(request.POST.get('star'))}
      )
      return HTTPResponse(status=201)
    else:
      return HTTPResponse(status=400)

class Search(ListView):
  """Поиск фильмов"""
  paginate_by = 3 

  def get_queryset(self):
    return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["q"] = f'q={self.request.GET.get("q")}&'
    return context



    