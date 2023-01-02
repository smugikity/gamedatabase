from django.urls import path,include,re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('brand-list',views.brand_list,name='brand-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    # End
    # Wishlist
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    # My AddressBook
    path('my-addressbook',views.my_addressbook, name='my-addressbook'),
    path('add-address',views.save_address, name='add-address'),
    path('activate-address',views.activate_address, name='activate-address'),
    path('update-address/<int:id>',views.update_address, name='update-address'),
    path('edit-profile',views.edit_profile, name='edit-profile'),

    # Edited
    path('list/<str:custom>',views.custom_list,name='list'),
    path('src/list/<str:custom>',views.src_custom_list,name='src-list'),
    path('game-list',views.game_list,name='game-list'),
    path('src/game-list',views.src_game_list,name='src-game-list'),
    path('search/<str:custom>',views.search,name='search'),
    path('custom-search/<str:custom>',views.custom_search_list,name='custom-search'),
    path('game-search',views.game_search_list,name='game-search'),
    path('view/<str:custom>/<int:id>',views.view_item,name='view'),
    path('view/game/<int:id>',views.game_detail,name='game-detail'),
    re_path(r'profile/(?P<username>\w+)/$',views.profile,name='profile'),
    path('p-list/<int:id>',views.personal_list,name='personal-list'),
    path('404',views.handler404,name='404'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)