from main.models import Game, Rating, Developer, Publisher, Platform,Genre,PersonalList
from django.db.models import Max,Min,Count,Avg,Q,OuterRef,F,Exists,Value,IntegerField,Subquery
from django.db.models.functions import Lower,JSONObject
from django.contrib.postgres.expressions import ArraySubquery
import numpy as np
from math import ceil

def get_n_random_games(n,user=None):
	query_list = Game.objects.all().annotate(genre_list=ArraySubquery(subquery_game_genre)).annotate(n_ratings=Count('rating'))
	if user: 
		wishlist_id = PersonalList.objects.filter(user=user).first().id
		s_query = PersonalList.objects.filter(pk=wishlist_id,game__id=OuterRef("pk"))
		query_list = query_list.annotate(is_favorited=Exists(s_query)).values('id','title','image','avg_rating','n_ratings','genre_list','is_favorited')
	else: query_list = query_list.values('id','title','image','avg_rating','n_ratings','genre_list')
	return np.random.choice(query_list, n, replace=False)

# Custom list of Models
CUSTOM_NAME=['game','genre','developer','publisher','platform']
CUSTOM_MODEL_ID={
    'genre': 1,
    'developer': 2,
    'publisher': 3,
    'platform': 4,
	'game': 0,
}
CUSTOM_LIST={
    'genre': Genre,
	CUSTOM_MODEL_ID['genre']: Genre,
    'developer': Developer,
	CUSTOM_MODEL_ID['developer']: Developer,
    'publisher': Publisher,
	CUSTOM_MODEL_ID['publisher']:Publisher,
    'platform': Platform,
	CUSTOM_MODEL_ID['platform']: Platform,
	'game': Game,
	CUSTOM_MODEL_ID['game']: Game,
}
SORT=['id','title']

subquery_game_genre = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(model_id=CUSTOM_MODEL_ID['genre'],id=F("id"), title=F("title"))).values_list("data")
subquery_game_developer = Developer.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(model_id=CUSTOM_MODEL_ID['developer'],id=F("id"), title=F("title"))).values_list("data")
subquery_game_platform = Platform.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(model_id=CUSTOM_MODEL_ID['platform'],id=F("id"), title=F("title"))).values_list("data")

subquery_rating_game = Game.objects.filter(pk=OuterRef("game")).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery_game_genre)).annotate(data=JSONObject(id=F("id"),title=F("title"),avg_rating=F("avg_rating"),n_ratings=F("n_ratings"),image=F("image"),genre_list=F("genre_list"))).values_list("data")[:1]

def get_search(custom,term):
	models = CUSTOM_LIST[custom]
	if (not models): return None
	data = models.objects.filter(title__istartswith=term).order_by('-id').values('id','title')
	data = list(data)
	return len(data), data

def get_custom_search(custom,sort,n_per,page,term):
	models = CUSTOM_LIST[custom]
	query_list = models.objects.filter(title__istartswith=term).annotate(model_id=Value(CUSTOM_MODEL_ID[custom], output_field=IntegerField()))
	return get_by_page(query_list,sort,n_per,page,'id','title','image','model_id')

def get_game_search(sort,n_per,page,term,model_list=Game.objects,user=None):
	query_list = model_list.filter(title__istartswith=term).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery_game_genre))#.annotate(dev_list=ArraySubquery(subquery_game_developer)).annotate(plat_list=ArraySubquery(subquery_game_platform))
	# favorited annotate check if its in wishlist (for heart button)
	if user: 
		wishlist_id = PersonalList.objects.filter(user=user).first().id
		s_query = PersonalList.objects.filter(pk=wishlist_id,game__id=OuterRef("pk"))
		query_list = query_list.annotate(is_favorited=Exists(s_query))
	if (user):
		return get_by_page(query_list,sort,n_per,page,'id','title','image','avg_rating','n_ratings','genre_list','is_favorited')
	return get_by_page(query_list,sort,n_per,page,'id','title','image','avg_rating','n_ratings','genre_list')

def get_custom_list(custom,sort,n_per,page):
	models = CUSTOM_LIST[custom]
	query_list = models.objects.all().annotate(model_id=Value(CUSTOM_MODEL_ID[custom], output_field=IntegerField()))
	return get_by_page(query_list,sort,n_per,page,'id','title','image','model_id')

def get_game_list(sort,n_per,page,startdate,enddate,genres,publishers,platforms,model_list=Game.objects,user=None):
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
	query_list = model_list.filter(query).annotate(n_ratings=Count('rating')).annotate(genre_list=ArraySubquery(subquery_game_genre))#.annotate(dev_list=ArraySubquery(subquery_game_developer)).annotate(plat_list=ArraySubquery(subquery_game_platform))
	# favorited annotate check if its in wishlist (for heart button)
	if user: 
		wishlist_id = PersonalList.objects.filter(user=user).first().id
		s_query = PersonalList.objects.filter(pk=wishlist_id,game__id=OuterRef("pk"))
		query_list = query_list.annotate(is_favorited=Exists(s_query))
	if (user):
		return get_by_page(query_list,sort,n_per,page,'id','title','image','avg_rating','n_ratings','genre_list','is_favorited')
	return get_by_page(query_list,sort,n_per,page,'id','title','image','avg_rating','n_ratings','genre_list')


def get_rating(sort,n_per,page,by_user=None,by_game=None):
	if by_game: 
		query_list = Rating.objects.filter(game=by_game)
		query_list = query_list.annotate(username=F('user__username'),pfp=F('user__profile__image'))
		return get_by_page(query_list,sort,n_per,page,'review_rating','review_title','review_text','username','pfp')
	elif by_user:
		query_list = Rating.objects.filter(user=by_user)
		query_list = query_list.annotate(game_detail=Subquery(subquery_rating_game))
		return get_by_page(query_list,sort,n_per,page,'review_rating','review_title','review_text','game_detail')

	else: return

	
def get_by_page(query_list,sort,n_per,page,*args):
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
	elif (sort == 3):
		data = query_list.order_by('-avg_rating')[start:end]
	else: return None
	return count,max_page,page,data.values(*args)
	 
def get_custom_item(custom,id):
	models = CUSTOM_LIST[custom]
	object = models.objects.get(pk=id).__dict__
	data =  {k: v for k, v in object.items() if (k!='_state' and k!='status')}
	data['custom'] = CUSTOM_NAME[custom]
	return data