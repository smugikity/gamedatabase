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
def get_list(custom,sort,n_per,page):
	models = CUSTOM_LIST[custom]
	if (not models or (sort > 2 or sort < 0)): return None
	count = models.objects.count()
	max_page = ceil(count/n_per)
	if (page<1): page=1
	if (page>max_page): page=max_page
	start = n_per*(page-1); end = n_per*page
	if (sort == 0):
		data = models.objects.all().order_by('id').values('id','title','image')[start:end]
	elif (sort == 1):
		data = models.objects.all().order_by(Lower('title')).values('id','title','image')[start:end]
	else:
		data = models.objects.annotate(num=Count('game')).order_by('-num').values('id','title','image')[start:end]
	return count, max_page, page, data

def get_search(custom,term):
	models = CUSTOM_LIST[custom]
	if (not models): return None
	data = models.objects.filter(title__istartswith=term).order_by('-id').values('id','title')
	data = list(data)
	return len(data), data

def get_custom_search(custom,term):
	models = CUSTOM_LIST[custom]
	data = models.objects.filter(title__istartswith=term).order_by('-id').values('id','title','image')
	count = len(data)
	# if (count==0): max_page=1
	# else: max_page=1
	return count, 1, 1, data

def get_game_search(term):
	subquery1 = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	subquery2= Developer.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	subquery3 = Platform.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	data = Game.objects.filter(title__istartswith=term).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery1)).annotate(dev_list=ArraySubquery(subquery2)).annotate(plat_list=ArraySubquery(subquery3)).order_by('-id').values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')
	count = len(data)
	# if (count==0): max_page=0
	# else: max_page=1
	return count, 1, 1, data

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
	subquery1 = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	subquery2= Developer.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	subquery3 = Platform.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
	query_list = Game.objects.filter(query).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery1)).annotate(dev_list=ArraySubquery(subquery2)).annotate(plat_list=ArraySubquery(subquery3))
	count = query_list.count()
	max_page = ceil(count/n_per)
	if (max_page==0): return 0,0,1,[]
	if (page<1): page = 1
	if (max_page<page): page = max_page
	start = n_per*(page-1); end = n_per*page
	if (sort == 0):
		data = query_list.order_by('id').values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')[start:end]
	elif (sort == 1):
		data = query_list.order_by(Lower('title')).values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')[start:end]
	elif (sort == 2):
		data = query_list.annotate(num=Count('rating')).order_by('-num').values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')[start:end]
	elif (sort == 3):
		data = query_list.order_by('-avg_rating').values('id','title','image','avg_rating','n_ratings','genre_list','dev_list','plat_list')[start:end]
	return count, max_page, page, data

def get_custom_item(custom,id):
	models = CUSTOM_LIST[custom]
	object = models.objects.get(pk=id).__dict__
	data =  {k: v for k, v in object.items() if (k!='_state' and k!='status')}
	data['custom'] = custom
	return data