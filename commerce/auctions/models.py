from django.contrib.auth.models import AbstractUser
from django.db import models



from django.utils import timezone
# now =  datetime.now()
# now = str(now)
# now = re.findall(r"(.+)\..+", now)
# now = str(now[0])

# user
class User(AbstractUser):
    pass

# category
class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")
    


# listings
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageUrl = models.TextField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    created_at = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchList")

    def __str__(self):
        return self.title


# comments
class Comment(models.Model):

    message = models.CharField(max_length=1300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    
    
    def __str__(self):
        return f"{self.who}"
































# list = ['All Categories', 'Antiques', 'Art', 'Baby', 'Books', 'Business &amp; Industrial', 'Cameras &amp; Photo', 'Cell Phones &amp; Accessories', 'Clothing, Shoes &amp; Accessories', 'Coins &amp; Paper Money', 'Collectibles', 'Computers/Tablets &amp; Networking', 'Consumer Electronics', 'Crafts', 'Dolls &amp; Bears', 'DVDs &amp; Movies', 'eBay Motors', 'Entertainment Memorabilia', 'Gift Cards &amp; Coupons', 'Health &amp; Beauty', 'Home &amp; Garden', 'Jewelry &amp; Watches', 'Music', 'Musical Instruments &amp; Gear', 'Pet Supplies', 'Pottery &amp; Glass', 'Real Estate', 'Specialty Services', 'Sporting Goods', 'Sports Mem, Cards &amp; Fan Shop', 'Stamps', 'Tickets &amp; Experiences', 'Toys &amp; Hobbies', 'Travel', 'Video Games &amp; Consoles', 'Everything Else']
# objects = [Category(categoryName=value) for value in list]

# Category.objects.bulk_create(objects)