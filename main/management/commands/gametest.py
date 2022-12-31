from django.core.management.base import BaseCommand
from django.contrib.postgres.aggregates import ArrayAgg
import unittest

class Command(BaseCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(GameListTestCase)
        unittest.TextTestRunner().run(suite)


class GameListTestCase(unittest.TestCase):
    def setUp(self):
        print("Write your pre-test prerequisites here")

    def test(self):
        from main.models import Game, Rating, Developer, Publisher, Platform, Genre 
        from django.db.models import Max,Min,Count,Avg,Q,OuterRef,F
        from django.db.models.functions import JSONObject,Lower
        from django.contrib.postgres.expressions import ArraySubquery
        from math import ceil

        sort,n_per,page,startdate,enddate,genres,publishers,platforms = 2,100,1,'1000-01-01','9999-12-31',[1,2,3],[1,2,3],[1,2,3]

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
        print(query)
        
        subquery1 = Genre.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
        subquery2= Developer.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
        subquery3 = Platform.objects.filter(game__id=OuterRef("pk")).annotate(data=JSONObject(id=F("id"), title=F("title"))).values_list("data")
        query_list = Game.objects.filter(query).annotate(genre_list=ArraySubquery(subquery1)).annotate(dev_list=ArraySubquery(subquery2)).annotate(plat_list=ArraySubquery(subquery3))
        count = query_list.count()

        max_page = ceil(count/n_per)
        if (page<1): page = 1
        if (max_page<page): page = max_page
        start = n_per*(page-1); end = n_per*page
        if (sort == 0):
            data = query_list.order_by('id').values('id','title','image','avg_rating','genre_list','dev_list','plat_list')[start:end]
        elif (sort == 1):
            data = query_list.order_by(Lower('title')).values('id','title','image','avg_rating','genre_list','dev_list','plat_list')[start:end]
        elif (sort == 2):
            print(query_list.annotate(num=Count('rating')).order_by('-num').values('id','title','image','avg_rating','genre_list','dev_list','plat_list')[start:end].query)

            data = query_list.annotate(num=Count('rating')).order_by('-num').values('id','title','image','avg_rating','genre_list','dev_list','plat_list')[start:end]
        elif (sort == 3):
            data = query_list.order_by('-avg_rating').values('id','title','image','avg_rating','genre_list','dev_list','plat_list')[start:end]
            
        [print(nigger) for nigger in data]
        return count, max_page, data    