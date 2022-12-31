from django.test import TestCase
from main.models import Game, Rating, Developer, Publisher, Platform, Genre 
from django.db.models import Max,Min,Count,Avg,Q
from django.db.models.functions import Lower
from math import ceil
from functools import reduce
import operator


# Create your tests here.
class GameListTestCase(TestCase):
    # def setUp(self):
    #     return

    def test(self):
        sort,n_per,page,startdate,enddate,genres,publishers,platforms = 0,9,1,'01/01/0000','31/12/9999',[],[],[]

        if (sort > 3 or sort < 0): return None
        count = Game.objects.count()
        query = reduce(operator.and_,[
            Q(release_date__gte=startdate),Q(release_date__lte=enddate),
            reduce(operator.or_,[Q(genre__id=genre_id) for genre_id in genres]),
            reduce(operator.or_,[Q(developer__publisher__id=publisher_id) for publisher_id in publishers]),
            reduce(operator.or_,[Q(platform__id=platforms_id) for platforms_id in platforms])
        ])
        print(query)
        max_page = ceil(count/n_per)
        if (page<1): page = 1
        if (max_page<page): page = max_page
        start = n_per*(page-1); end = n_per*page
        if (sort == 0):
            data = Game.objects.all().order_by('id').values('id','title','image','avg_rating')[start:end]
        elif (sort == 1):
            data = Game.objects.all().order_by(Lower('title')).values('id','title','image','avg_rating')[start:end]
        elif (sort == 2):
            data = Game.objects.annotate(num=Count('rating')).order_by('-num').values('id','title','image','avg_rating')[start:end]
        
        return count, max_page, data