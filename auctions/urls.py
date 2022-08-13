from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("categories", views.list_categories, name="categories"),
    path("watchlist", views.get_watch_list, name="watchlist"),
    path("category/<str:category>", views.view_category_listings, name="category"),
]
