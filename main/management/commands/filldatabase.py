from django.core.management.base import BaseCommand
import random
import datetime
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

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
                b = Genre(title=generateRandomString(1,r), description=generateRandomString(20,r))
                save_image_from_url(b, 'https://picsum.photos/200/250',i+1)
                b.save()
        if (Publisher.objects.count()<30):
            for i in range(30):        
                b = Publisher(title=generateRandomString(2,r)+"games", description=generateRandomString(20,r))
                save_image_from_url(b, 'https://picsum.photos/200/250',i+1)
                b.save()
        if (Platform.objects.count()<30):
            for i in range(30):
                b = Platform(title=generateRandomString(1,r), description=generateRandomString(20,r))
                save_image_from_url(b, 'https://picsum.photos/200/250',i+1)
                b.save()
        if (Developer.objects.count()<30):
            for i in range(30):       
                b = Developer(title=generateRandomString(2,r)+"studio", description=generateRandomString(20,r),publisher=Publisher.objects.get(pk=random.randrange(1,30)))
                save_image_from_url(b, 'https://picsum.photos/200/250',i+1)
                b.save()
        if (Game.objects.count()<30):
            for i in range(30):
                b = Game(
                    title=generateRandomString(3,r), 
                    description=generateRandomString(20,r),
                    release_date=datetime.datetime(year=random.randrange(1000,2000), month=random.randrange(1,12), day=random.randrange(1,28)),
                    avg_rating=0,
                )
                save_image_from_url(b, 'https://picsum.photos/200/250',i+1)
                b.save()
                b.genre.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                b.developer.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                b.platform.add(random.randrange(1,30),random.randrange(1,30),random.randrange(1,30))
                
def save_image_from_url(model, url, i):
    r = requests.get(url)

    img_temp = NamedTemporaryFile()  
    img_temp.write(r.content)
    img_temp.flush()

    model.image.save(model.__class__.__name__+str(i)+".jpg", File(img_temp), save=True)    

def generateRandomString(n,r):
    des = ""
    for i in range(n):
        des += r.get_random_word()+" "
    return des
