from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, listings, Watchlist, bids, comments, categories
from .forms import CreateListing
from django.db import models
from django.db.models import Max


def index(request):
    view_listing = listings.objects.all()
    view = [viewing.format() for viewing in view_listing]
    return render(request, "auctions/index.html", {"Listings": view})

def view_listing(request, listing_id):
    try:
        watch_list = Watchlist.objects.filter(user_id=request.user.id, username=request.user.username, listing_id=listing_id).get()
    except:
        watch_list = None    

    if request.POST.get("bid", None):
        bid = bids(user_id = request.user.id, username = request.user.username, listing_id = listing_id, bid_amount = request.POST.get('bid'))
        bid.save()
    elif request.POST.get("watch_list", None):
        if not watch_list:
            watch_list = Watchlist(user_id=request.user.id, username=request.user.username, listing_id=listing_id, watched=True, listing_title=request.POST.get("list_title"))
            watch_list.save()
        elif watch_list.watched:
            watch_list.watched = False
        else:
            watch_list.watched = True
        watch_list.save()
    
    listing_to_view = listings.objects.filter(id=listing_id).get()
    if request.POST.get("close", None):
        listing_to_view.closed = True
    try:
        get_bids = bids.objects.filter(user_id = request.user.id, username = request.user.username, listing_id = listing_id).order_by('bid_amount').first().format()
        if not get_bids:
            get_bids = {
            "bid_amount": 0.00
            }
    except Exception as err:
        get_bids = {
            "bid_amount": 0.00
            }

    if request.POST.get('comment', None):
        comment = comments(user_id = request.user.id, username = request.user.username, listing_id = listing_id, title = request.POST.get('comment_title', 'Untitled'), comment = request.POST.get('comment'))
        comment.save()
    
    comments_to_list = comments.objects.filter(listing_id = listing_id).all()
    comment_completed = None
    if comments_to_list:
        comment_completed = [comment.format() for comment in comments_to_list]

    return render(request, "auctions/view_listing.html", {
        "listing": listing_to_view.format(),
        "watchlist": watch_list.format() if watch_list else None,
        "bids": get_bids,
        "max_bid": float(listing_to_view.format()['Starting_bid']) if float(listing_to_view.format()['Starting_bid']) > float(get_bids['bid_amount']) else float(get_bids['bid_amount']),
        "comments": comment_completed
    })

def list_categories(request):
    categories_to_view = categories.objects.all()
    return render(request, "auctions/categories.html",
        {
            "Category": [c.format() for c in categories_to_view]
        }
    )

@login_required
def get_watch_list(request):
    getWatchList = Watchlist.objects.filter(user_id=request.user.id).all()
    return render(request, "auctions/view_watchlist.html",
    {
        "watchlist": [list_watch.format() for list_watch in getWatchList],
    })

@login_required
def create_listing(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateListing(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Created_listing = listings(user_id = request.user.id, username = request.user.username,
    title = form.cleaned_data['title'], description = form.cleaned_data['description'], Starting_bid = form.cleaned_data['Starting_bid'], image_URL = form.cleaned_data['image_URL'], category = form.cleaned_data['category'])
            Created_listing.save()
            return HttpResponseRedirect(reverse("index"))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateListing()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def view_category_listings(request, category):
    get_listings = listings.objects.filter(category=category).all()
    return render(request, "auctions/view_listings_per_category.html",
    {
        "listings": [c.format() for c in get_listings]
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
