from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Genre,Publisher,Developer,Platform,Game,PersonalList,Rating,Comment,Profile,ACTIVE,INACTIVE,PRIVATE
from django.contrib import messages
from django.utils.translation import ngettext

# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)


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


