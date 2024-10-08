from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True),
        "categories": Category.objects.all()
        })

def displayCategory(request):
    if request.method == "POST":
        category = request.POST["category"]
        category = Category.objects.get(categoryName=category)        
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(isActive=True, category = category),
            "categories": Category.objects.all()
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

@login_required
def add(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        imageUrl = request.POST['imageUrl']
        price = request.POST['price']
        category = request.POST['category']
        owner = request.user
        category = Category.objects.get(categoryName=category)
        category.save()
        bid = Bid(bid=float(price), user=request.user)
        listing = Listing(title=title, description=description, imageUrl=imageUrl, category=category, owner=owner, price=bid)
        print("saving....")
        listing.save()
        print("saved")

    return render(request, "auctions/add.html", {
        "categories": Category.objects.all()
        })
    # if request.method == "POST":
    #     comment = request.POST['comment']
    #     comment = Comment(who=request.user, comment = comment)
    #     comment.save()



@login_required
def listing(request, listing_id):
    listingData = Listing.objects.get(id=listing_id)
    currentUser= request.user
    isListingInWatchList = request.user in listingData.watchlist.all()
    if request.method == "POST":
        print("POST request detected")
        if 'remove' in request.POST:
            print("Removing from watchlist")
            listingData.watchlist.remove(currentUser)
            isListingInWatchList = False
        elif 'add' in request.POST:
            print("Adding to watchlist")
            listingData.watchlist.add(currentUser)
            isListingInWatchList = True
        elif 'comment' in request.POST:
            message = request.POST.get("comment")
            comment = Comment(listing=listingData, author=currentUser, message=message)
            comment.save()
        return redirect('listing', listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "comments": Comment.objects.all()
        })

@login_required
def wishlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listingData = Listing.objects.get(id = listing_id)
        listingData.watchlist.remove(request.user)
           
  


    return render(request, "auctions/wishlist.html", {
        "listings": Listing.objects.filter(watchlist=request.user),
        "categories": Category.objects.all(),
        "user": request.user,
        })