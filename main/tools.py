from main.models import Game, Rating
from random import randint

def game_info(pid):
	game = Game.objects.get(pk=pid)
	if not game: return None
	data = {
		'title': game.title,
		'image': game.image,
		'avg_rating': game.avg_rating,
		'n_ratings': Rating.objects.filter(game=game).count(),
		'primary_genres': game.genre.all()[:3],
	}
	return data

def all_game_info():
	games = Game.objects.all()
	data = []
	for game in games:
		if game:
			data.append({
				'title': game.title,
				'image': game.image,
				'avg_rating': game.avg_rating,
				'n_ratings': Rating.objects.filter(game=game).count(),
				'primary_genres': game.genre.values('title'),
			})
	return data
	
def get_n_random_games(n):
	total = Game.objects.count()
	if total <= n:
		return all_game_info()
	random_games = []
	max_id = Game.objects.all().aggregate(max_id=Max("id"))['max_id']
	if max_id != None:
		iterated = []
		for x in range(0,n):
			pk = randint(1, max_id)
			if pk not in iterated:
				iterated.append(pk)
				game = game_info(pk)
				if game: random_games.append(game)
				else: n += 1
			else: n += 1
	return random_games