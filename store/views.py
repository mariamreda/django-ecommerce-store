from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Category,Profile, Order, ProductReview
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from .forms import SignUpForm, UserInfoForm,ProductReviewForm
from django import forms 
from django.db.models import Max, Min, Count, Avg, Sum, F, Q
from django.utils.timezone import now
from datetime import timedelta,date
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
import calendar



# def update_info(request):
# 	if request.user.is_authenticated:
# 		# Get Current User
# 		current_user = Profile.objects.get(user__id=request.user.id)
# 		# # Get Current User's Shipping Info
# 		# shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
# 		# Get original User Form
# 		form = UserInfoForm(request.POST or None, instance=current_user)
# 		# Get User's Shipping Form
# 		# shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
# 		if form.is_valid() :
# 			# Save original form
# 			form.save()
# 			# Save shipping form
# 			# shipping_form.save()

# 			messages.success(request, "Your Info Has Been Updated!!")
# 			return redirect('home')
# 		return render(request, "update_info.html", {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In To Access That Page!!")
# 		return redirect('home')



def dashboard4(request):
    reviews_count_per_category = (
        ProductReview.objects
        .values('category__name') 
        .annotate(reviews_count=Count('id')) 
        .order_by('category__name')
    )
    
    product_category_labels = [category['category__name'] for category in reviews_count_per_category]
    number_of_reviews = [category['reviews_count'] for category in reviews_count_per_category]
    
    return render(request, 'dashboard4.html', {
        'product_category_labels':product_category_labels,
        'number_of_reviews':number_of_reviews,
      
    })

def dashboard(request):
    #Quantity Sold Per Product
    product = Product.objects.all()
    orders = Order.objects.all()
    
    product_sales = {}
    for order in orders:
        if order.product.name in product_sales:
            product_sales[order.product.name] += order.quantity
        else:
            product_sales[order.product.name] = order.quantity
    
    product_labels = list(product_sales.keys())
    quantity_sold = list(product_sales.values())

    category_sales = (
        Order.objects
        .values('product__category__name') 
        .annotate(total_quantity=Sum('quantity')) 
        .order_by('product__category__name')
    )
    

    category_labels = [category['product__category__name'] for category in category_sales]
    quantity_sold_per_category = [category['total_quantity'] for category in category_sales]
    
    
    # Total Sales Revenue per Product
    revenue_per_product = (
        Order.objects
        .values('product__name') 
        .annotate(total_revenue=Sum(F('quantity') * F('product__price'))) 
        .order_by('-total_revenue')
    )
    
    
    revenue_product_labels = [revenue['product__name'] for revenue in revenue_per_product]
    revenue_per_product = [float(revenue['total_revenue']) for revenue in revenue_per_product]
    
    return render(request, 'dashboard.html', {
        'product': product_labels,
        'quantitySold': quantity_sold,
        'category': category_labels,
        'quantitySoldPerCategory': quantity_sold_per_category,
        'revenue_product_labels':revenue_product_labels,
        'revenue_per_product':revenue_per_product,
      
    })
    
    
     #product insights
def dashboard2(request):
    #Find the number of products in each category    
    product_count_per_category = (
        Product.objects
        .values('category__name') 
        .annotate(product_count=Count('id')) 
        .order_by('category__name')
    )
    product_category_labels = [category['category__name'] for category in product_count_per_category]

    number_of_products = [product['product_count'] for product in product_count_per_category]
    Product_sales = (
        Order.objects
        .values('product__name') 
        .annotate(total_quantity=Sum('quantity')) 
        .order_by('total_quantity')
    )
    

    
    
    
    return render(request, 'dashboard2.html', {
        'product_category_labels':product_category_labels,
        'number_of_products':number_of_products,
      
    })
    
    
    
    #Orders insights
def dashboard3(request):
    total_orders = Order.objects.count()
    # orders = Order.objects.all()
    category_sales = (
        Order.objects
        .values('product__category__name') 
        .annotate(total_quantity=Sum('quantity')) 
        .order_by('product__category__name')
    )
   
    orders_per_day = Order.objects.values('date').annotate(orders_count=Count('id')).order_by('date')
    
    days = [days['date'] for days in orders_per_day]
    orders_num = [c['orders_count'] for c in orders_per_day]
    days_strings = [d.strftime('%Y-%m-%d') for d in days]
	

    category_labels = [category['product__category__name'] for category in category_sales]
    quantity_sold_per_category = [category['total_quantity'] for category in category_sales]
    return render(request, 'dashboard3.html', {
        'total_orders':total_orders,
       	'category': category_labels,
        'quantitySoldPerCategory': quantity_sold_per_category,
        'days_strings':days_strings,
        'orders_num':orders_num,
        
    })





def search(request):
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})


def update_info(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('home')  
    else:
        form = UserInfoForm(user=request.user, instance=request.user.profile)

    return render(request, 'update_info.html', {'form': form})



def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	


def category(request, cat):
	# Replace Hyphens with Spaces
	cat = cat.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=cat)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    reviews = ProductReview.objects.filter(product=product)
    review_form= ProductReviewForm()
    make_review=True
    if request.user.is_authenticated:
        user_review_count=ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count>0:
            make_review=False
        
    return render(request, 'product.html', {'product': product, 
                                            'reviews': reviews,
                                            'review_form':review_form,
                                            'make_review':make_review,})

def ajax_add_review(request, pid):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pid)
        user = request.user

        review = ProductReview.objects.create(
            user=user,
            product=product,
            review=request.POST['review'],
            rating=int(request.POST['rating']),
        )

        context = {
            'user': user.username,
            'review': request.POST['review'],
            'rating': request.POST['rating'],
        }

        return JsonResponse({'bool': True, 'context': context})

    return JsonResponse({'bool': False})
    
    


def home(request):
    products= Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your Profile Info..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})


