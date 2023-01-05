from django.contrib import admin
from .models import Banner,Genre,Publisher,Developer,Platform,Game,PersonalList,Rating,Comment,Profile,ACTIVE,INACTIVE,PRIVATE
from django.contrib import messages
from django.utils.translation import ngettext


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

# Edited
@admin.action(description='Mark selected active')
def set_status_active(self, request, queryset):
    updated=queryset.update(status=ACTIVE)
    self.message_user(request, ngettext('%d object was successfully marked as active.','%d objects were successfully marked as active.',updated) % updated, messages.SUCCESS)

@admin.action(description='Mark selected inactive')
def set_status_inactive(self, request, queryset):
    updated=queryset.update(status=INACTIVE)
    self.message_user(request, ngettext('%d story was successfully marked as inactive.','%d objects were successfully marked as inactive.',updated) % updated, messages.SUCCESS)

@admin.action(description='Mark selected private')
def set_status_private(self, request, queryset):
    updated=queryset.update(status=PRIVATE)
    self.message_user(request, ngettext('%d story was successfully marked as private.','%d objects were successfully marked as private.',updated) % updated, messages.SUCCESS)

class GenreAdmin(admin.ModelAdmin):
	list_display=('id','title','description','get_parent_genre','status')
	actions=(set_status_active,set_status_inactive,set_status_private)
admin.site.register(Genre,GenreAdmin)

class PublisherAdmin(admin.ModelAdmin):
	list_display=('id','title','description','image_tag','status')
	actions=(set_status_active,set_status_inactive,set_status_private)
admin.site.register(Publisher,PublisherAdmin)

class DeveloperAdmin(admin.ModelAdmin):
	list_display=('id','title','description','image_tag','status')
	actions=(set_status_active,set_status_inactive,set_status_private)
admin.site.register(Developer,DeveloperAdmin)

class PlatformAdmin(admin.ModelAdmin):
    list_display=('id','title','description','image_tag','status')
    actions=(set_status_active,set_status_inactive,set_status_private)
admin.site.register(Platform,PlatformAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display=('id','title','description','image_tag','status')
    list_edit=('id','title','description','genre','developer','platform','image','status')
    actions=(set_status_active,set_status_inactive,set_status_private)
admin.site.register(Game,GameAdmin)

class PersonalListAdmin(admin.ModelAdmin):
	list_display=('id','title','description','user')
admin.site.register(PersonalList,PersonalListAdmin)

class RatingAdmin(admin.ModelAdmin):
	list_display=('id','user','game','review_rating','review_text')
admin.site.register(Rating,RatingAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display=('id','user','game','content')
admin.site.register(Comment,CommentAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display=('id','user','image','bio','country')
admin.site.register(Profile,ProfileAdmin)


