from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from main.models import UserSession

def remove_other_sessions(sender, user, request, **kwargs):
    remove_all_sessions(sender, user, request, **kwargs)
    request.session.save()
    UserSession.objects.get_or_create(session_id=request.session.session_key, defaults={"user": user})

def remove_all_sessions(sender, user, request, **kwargs):
    if user is not None:
        Session.objects.filter(usersession__user=user).delete()

user_logged_in.connect(remove_other_sessions)
user_logged_out.connect(remove_all_sessions)