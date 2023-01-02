from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from main.models import UserSession
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from main.models import Profile,PersonalList

def remove_other_sessions(sender, user, request, **kwargs):
    remove_all_sessions(sender, user, request, **kwargs)
    request.session.save()
    UserSession.objects.get_or_create(session_id=request.session.session_key, defaults={"user": user})

def remove_all_sessions(sender, user, request, **kwargs):
    if user is not None:
        Session.objects.filter(usersession__user=user).delete()

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        PersonalList.objects.create(user=instance,title="Wishlist")
        print("Created user with profile and wishlist")

user_logged_in.connect(remove_other_sessions)
user_logged_out.connect(remove_all_sessions)
post_save.connect(create_profile, sender=User)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
