from django.core.management.base import BaseCommand
import random
import datetime

class Command(BaseCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle(self, **options):
        from main.models import Game, Rating, Developer, Publisher, Platform, Genre 
        from random_word import RandomWords
        from main.models import STATUS
        
        r = RandomWords()

        if (Genre.objects.count()<30):
            for i in range(30):
                b = Genre(title=r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word(), description=r.get_random_word())
                b.save()
        if (Publisher.objects.count()<30):
            for i in range(30):        
                b = Publisher(title=r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word(), description=r.get_random_word())
                b.save()
        if (Platform.objects.count()<30):
            for i in range(30):
                b = Platform(title=r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word(), description=r.get_random_word())
                b.save()
        if (Developer.objects.count()<30):
            for i in range(30):       
                b = Developer(title=r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word(), description=r.get_random_word(),publisher=Publisher.objects.get(pk=random.randrange(1,30)))
                b.save()
        if (Game.objects.count()<30):
            for i in range(30):
                b = Game(
                    title=r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word(), 
                    description=r.get_random_word(),
                    release_date=datetime.datetime(year=random.randrange(1000,2000), month=random.randrange(1,12), day=random.randrange(1,28)),
                    avg_rating=random.randrange(50)/10,
                )
                b.save()
                b.genre.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                b.developer.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                b.platform.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                
            