from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

#Edited

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_imgs/default.png', upload_to='profile_imgs')
    bio = models.TextField(default='Hi! I\'m using Game Database. <3')
    country = models.CharField(max_length=60,default='Russia',null=True,blank=True)
    
    class Meta:
        verbose_name_plural='Profiles'
    def __str__(self):
        return self.user.username

# User session
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, primary_key=True, related_name="usersessions", related_query_name="usersession")
    class Meta:
        verbose_name_plural='User Sessions'

# Status:
INACTIVE = 0
ACTIVE = 1
PRIVATE = 2

STATUS=(
    (INACTIVE, 'Inactive'),
    (ACTIVE, 'Active'),
    (PRIVATE, 'Private'),
)

# Genre
class Genre(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    parent_genre=models.ForeignKey('self',blank=True,null=True,on_delete=models.SET_NULL)
    image=models.ImageField(upload_to="genre_imgs/",blank=True,null=True)
    status=models.PositiveSmallIntegerField(choices=STATUS,default=INACTIVE)

    class Meta:
        verbose_name_plural='Genres'

    def get_parent_genre(self):
        if self.parent_genre == None: return ""
        return self.parent_genre.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Publisher
class Publisher(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    founding_year=models.DateField(blank=True,null=True)
    website=models.URLField(blank=True,null=True)
    image=models.ImageField(upload_to="publisher_imgs/",blank=True,null=True)
    status=models.PositiveSmallIntegerField(choices=STATUS,default=INACTIVE)

    class Meta:
        verbose_name_plural='Publishers'

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))

# Developer
class Developer(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    founding_year=models.DateField(blank=True,null=True)
    website=models.URLField(blank=True,null=True)
    image=models.ImageField(upload_to="developer_imgs/",blank=True,null=True)
    publisher=models.ForeignKey(Publisher,blank=True,null=True,on_delete=models.SET_NULL)
    status=models.PositiveSmallIntegerField(choices=STATUS,default=INACTIVE)

    class Meta:
        verbose_name_plural='Developers'

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Platform
class Platform(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="platform_imgs/",blank=True,null=True)
    status=models.PositiveSmallIntegerField(choices=STATUS,default=INACTIVE)

    class Meta:
        verbose_name_plural='Platforms'

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Game
class Game(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    release_date=models.DateField(blank=True,null=True)
    genre=models.ManyToManyField(Genre,blank=True)
    developer=models.ManyToManyField(Developer,blank=True)
    platform=models.ManyToManyField(Platform,blank=True)
    image=models.ImageField(upload_to="game_imgs/",blank=True,null=True)
    avg_rating=models.FloatField(default=0)
    status=models.PositiveSmallIntegerField(choices=STATUS,default=INACTIVE)

    class Meta:
        verbose_name_plural='Games'

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Personal List
class PersonalList(models.Model):
    title=models.CharField(max_length=200,blank=False,null=False)
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    game=models.ManyToManyField(Game,blank=True)

    class Meta:
        verbose_name_plural='Personal Lists'
    def __str__(self):
        return self.title

# Rating Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

# Rating
class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    game=models.ForeignKey(Game,on_delete=models.CASCADE)
    review_rating=models.SmallIntegerField(choices=RATING,max_length=150)
    review_title=models.CharField(max_length=200,blank=True)
    review_text=models.TextField(blank=True)

    class Meta:
        verbose_name_plural='Ratings'

    def get_review_rating(self):
        return self.review_rating

# Comment
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    game=models.ForeignKey(Game,on_delete=models.CASCADE)
    content=models.TextField()

    class Meta:
        verbose_name_plural='Comments'

