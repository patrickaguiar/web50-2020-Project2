from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('create_listing', views.create_listing, name='create_listing'),
    path('my_listings', views.my_listings, name='my_listings'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('most_commented', views.most_commented, name='most_commented'),
    path('star', views.star, name='star'),
    path('categories', views.categories, name='categories'),
    path('categories/<category_id>', views.categories_id, name='categories_id'),
    path('item/<item_id>', views.item, name='item'),
    path('oferta', views.oferta, name='oferta'),
    path('comentario', views.comentario, name='comentario'),
    path('add_watchlist/<item_id>', views.add_watchlist, name='add_watchlist'),
    path('remove_watchlist/<item_id>', views.remove_watchlist, name='remove_watchlist'),
    path('edit_listing/<item_id>', views.edit_item, name='edit_listing'),
    path('delete_listing', views.delete_listing, name='delete_listing')
]