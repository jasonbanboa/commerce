from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.filter, name="filter"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove", views.remove_watchlist, name="remove_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
]
    