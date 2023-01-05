from django.urls import path,include,re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('accounts/signup',views.signup,name='signup'),
    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    # End
    path('edit-profile',views.edit_profile, name='edit-profile'),

    # Edited
    path('list/<str:custom>',views.custom_list,name='list'),
    path('src/list/<str:custom>',views.src_custom_list,name='src-list'),
    path('game-list',views.game_list,name='game-list'),
    path('src/game-list',views.src_game_list,name='src-game-list'),
    path('search/<str:custom>',views.search,name='search'),
    path('src/custom-search/<str:custom>',views.custom_search_list,name='custom-search'),
    path('src/game-search',views.game_search_list,name='game-search'),
    path('view/<int:model_id>/<int:id>',views.view_item,name='view'),
    path('view/game/<int:id>',views.game_detail,name='game-detail'),
    re_path(r'profile/(?P<username>\w+)/$',views.profile,name='profile'),
    path('404',views.handler404,name='404'),
    #Personal list
    path('p-list/<int:id>',views.personal_list,name='personal-list'),
    path('p-list/<int:id>/add',views.personal_list_add,name='personal-list-add'),
    path('p-list/<int:id>/remove',views.personal_list_remove,name='personal-list-remove'),
    path('p-list/wishlist',views.wishlist,name='personal-list'),
    path('p-list/wishlist/add',views.wishlist_add,name='personal-list-add'),
    path('p-list/wishlist/remove',views.wishlist_remove,name='personal-list-remove'),
    path('comment/add',views.comment_add,name='comment-add'),
    path('review/add',views.review_add,name='review-add'),
    path('review/delete',views.review_delete,name='review-delete'),
    #Rating
    path('rating',views.get_rating,name='get-rating'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)