from main.models import Game, Rating, Developer, Publisher, Platform, Genre 
from django.db.models import Max,Min,Count,Avg,Q,OuterRef,F
from django.db.models.functions import Lower,JSONObject
from django.contrib.postgres.expressions import ArraySubquery
import numpy as np
from math import ceil

def get_n_random_games(n):
	subquery1 = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	data = Game.objects.all().annotate(genre_list=ArraySubquery(subquery1)).annotate(n_ratings=Count('rating')).order_by('-id').values('id','title','image','avg_rating','n_ratings','genre_list')
	random_games = np.random.choice(data, n, replace=True)
	return random_games

# Custom list of Models
CUSTOM_LIST={
    'genre': Genre,
    'developer': Developer,
    'publisher': Publisher,
    'platform': Platform,
	'game': Game,
}
SORT=['id','title']
subquery_game_genre = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
subquery_game_developer = Developer.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
subquery_game_platform = Platform.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")

def get_search(custom,term):
	models = CUSTOM_LIST[custom]
	if (not models): return None
	data = models.objects.filter(title__istartswith=term).order_by('-id').values('id','title')
	data = list(data)
	return len(data), data

def get_custom_search(custom,sort,n_per,page,term):
	models = CUSTOM_LIST[custom]
	query_list = models.objects.filter(title__istartswith=term)
	return get_by_page(query_list,sort,n_per,page,False)

def get_game_search(sort,n_per,page,term):
	query_list = Game.objects.filter(title__istartswith=term).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery_game_genre)).annotate(dev_list=ArraySubquery(subquery_game_developer)).annotate(plat_list=ArraySubquery(subquery_game_platform))
	return get_by_page(query_list,sort,n_per,page,True)

def get_list(custom,sort,n_per,page):
	models = CUSTOM_LIST[custom]
	query_list = models.objects.all()
	return get_by_page(query_list,sort,n_per,page,False)

def get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms):
	if (sort > 3 or sort < 0): return None
	query =  Q(release_date__gte=startdate) & Q(release_date__lte=enddate)
	if (len(genres)>0):
		query &= Q(genre__id=genres[0])
		for thing in genres[1:]:
			query |= Q(genre__id=thing)
	if (len(publishers)>0):
		query &= Q(developer__publisher__id=publishers[0])
		for thing in publishers[1:]:
			query |= Q(developer__publisher__id=thing)
	if (len(platforms)>0):
		query &= Q(platform__id=platforms[0])
		for thing in platforms[1:]:
			query |= Q(platform__id=thing)
	query_list = Game.objects.filter(query).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery_game_genre)).annotate(dev_list=ArraySubquery(subquery_game_developer)).annotate(plat_list=ArraySubquery(subquery_game_platform))
	return get_by_page(query_list,sort,n_per,page,True)

def get_by_page(query_list,sort,n_per,page,is_game):
	count = query_list.count()
	max_page = ceil(count/n_per)
	if (max_page==0): return 0,1,1,[]
	if (page<1): page = 1
	if (max_page<page): page = max_page
	start = n_per*(page-1); end = n_per*page
	if (sort == 0):
		data = query_list.order_by('id')[start:end]
	elif (sort == 1):
		data = query_list.order_by(Lower('title'))[start:end]
	elif (sort == 2):
		data = query_list.annotate(num=Count('rating'))[start:end]
	elif (is_game and sort == 3):
		data = query_list.order_by('-avg_rating')[start:end]
	else: return None
	if (is_game): return count,max_page,page,data.values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')
	else: return count,max_page,page,data.values('id','title','image')
	 
def get_custom_item(custom,id):
	models = CUSTOM_LIST[custom]
	object = models.objects.get(pk=id).__dict__
	data =  {k: v for k, v in object.items() if (k!='_state' and k!='status')}
	data['custom'] = custom
	return data