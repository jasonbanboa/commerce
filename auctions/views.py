from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment
from .forms import CommentForm



def index(request):
    listings_won = False
    if request.user.is_authenticated:
        listings = Listing.objects.all().filter(active=True)
        bids = Bid.objects.all()
        
        return render(request, "auctions/index.html", {
            "listings": listings,
            "valid": True,
            "bids": bids,
            "listings_won": listings_won,
    })
    return render(request, "auctions/index.html")


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
        except ValueError:
            return render(request, "auctions/register.html", {
                "message": "Please fill out the form to register"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        listing = Listing()
        listing.user = request.user.username
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.category = str(request.POST.get('category')).capitalize()
        listing.starting_bid = request.POST.get('starting_bid')
        listing.url = request.POST.get('url')
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")


@login_required
def listing(request, listing_id):
    comments = Comment.objects.all().filter(listing_id=listing_id)
    form = CommentForm()
    listing = Listing.objects.get(id=listing_id)
    status = listing.active
    user = request.user.username
    owner = False
    watchers = listing.watchlist.all()
    
    watching = False
    
    user_ob = User.objects.get(username=request.user.username)
    won = Listing.objects.all().filter(winner=user_ob, id=listing.id) 
    
    for u in watchers:
        if u.username == user:
            watching = True
    
    if listing.user == user:
        owner = True
        
    bids = Bid.objects.all().filter(listings=listing)
    highest_bid = bids.order_by('-bid').first()
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "owner": owner,
        "highest_bid": highest_bid,
        "watching": watching,
        "form": form,
        "comments": comments,
        "status": status,
        "won": won,
        
    })
    
    
@login_required
def categories(request):
    categories = []
    
    temp = Listing.objects.values_list("category" ,flat=True)
    for i in temp:
        if i == None or i == '':
            continue
        
        if str(i).capitalize() not in categories:
            categories.append(str(i).capitalize())
    
        
    return render(request, "auctions/categories.html", {
        "categories": categories,
        
    })
    

@login_required
def filter(request, category):
    return render(request, "auctions/filter.html", {
        "listings": Listing.objects.all().filter(category=category),
        "category": category
    })
    
       
@login_required
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    listings = Listing.objects.all().filter(watchlist=user)
    if request.method == "POST":
        item = Listing.objects.get(id=int(request.POST.get("id")))
        item.watchlist.add(user)
        item.save()
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
        })
    return render(request, "auctions/watchlist.html", {
            "listings": listings,
        })


@login_required
def remove_watchlist(request):
    user = User.objects.get(username=request.user.username)
    
    if request.method == "POST":
        item = Listing.objects.get(id=int(request.POST.get("id")))
        item.watchlist.remove(user)
        item.save()
        return redirect("watchlist")

 
def bid(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        listing = Listing.objects.get(id=int(listing_id))
        try:
            bid_price = float(request.POST.get("bid"))
            bids = Bid.objects.all().filter(listings=listing)
            
            highest_bid = bids.order_by('-bid').first()
            if highest_bid == None:
                highest_bid = listing

                if bid_price < float(highest_bid.starting_bid): 
                    raise EOFError
            else:
                if bid_price <= float(highest_bid.bid):
                    raise EOFError
                    
            
            bid = Bid(user=user, listings=listing, bid=bid_price)
            bid.save()
            listing.highest = bid
            listing.save()
        except ValueError:
            messages.add_message(request, messages.INFO, 'You can not bid nothing')

        except EOFError:
             messages.add_message(request, messages.INFO, 'You can only bid higher than the current bid')

        return redirect("listing", listing_id)


def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            cmnt = form.cleaned_data["comment"]
            comment = Comment(listing=listing, user=user, comment=cmnt)
            comment.save()
        
    return redirect("listing", listing_id)


def close_listing(request, listing_id):
    user = request.user.username
    listing = Listing.objects.get(id=listing_id)
    if user == listing.user:
        if listing.highest != None:
            listing.winner = listing.highest.user
        else:
            pass
        listing.active = False
        listing.save()
    return redirect("index")




# make owns of listing be able to close the listing
# when listing is closed the higest bidder gets a alert saying they won