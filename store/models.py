from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

RATING=(
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
# Create Customer Profile
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    phone = models.CharField(max_length=10, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    # first_name = models.CharField(max_length=50,null=True, blank=True )
    # last_name = models.CharField(max_length=50, null=True, blank=True )
    # email = models.EmailField(max_length=254,null=True, blank=True )

    def __str__(self):
        return self.user.username


    
    # Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)



#categories of products
class Category(models.Model):
    name= models.CharField(max_length=50)
    
    def __str__(self):
        return self.name #to appear on admin page
    
    
    class Meta:
        verbose_name_plural='categories'




class Product (models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2, max_digits=6)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1 )
    description=models.CharField(max_length=50, default='', blank=True, null=True)
    image=models.ImageField(upload_to='uploads/product/')
    is_sale= models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name
    
#customer orders
class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100, default='', blank=True)
    phone=models.CharField(max_length=20, default='', blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product}"
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews")
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review= models.TextField()
    rating=models.IntegerField(choices=RATING, default=None)
    date=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural='Product Reviews'
    
    
    def __str__(self):
        return f"{self.product.name}"
    
    def get_rating(self):
        return self.rating
    