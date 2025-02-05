from django.shortcuts import render, get_object_or_404,redirect
from .cart import Cart #cart class in cart.py 
from store.models import Order, Product,Profile
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone





def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	# totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities})

def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response



@login_required
def checkout(request):
    if request.method == "POST":
        user = request.user  

        # try:
        #     Profile = Profile.objects.get(last_name=user.last_name) 
        # except Profile.DoesNotExist:
        #     messages.error(request, "Customer not found.")
        #     return redirect("cart_summary")

        try:
            profile = Profile.objects.get(user=user)
            address = profile.address1
            phone = profile.phone
        except Profile.DoesNotExist:
            messages.error(request, "Profile details are missing. Please update your information.")
            return redirect("update_info")

        cart = Cart(request)

        cart_items = cart.get_prods()  
        quantities = cart.get_quants()  

        if not cart_items:
            messages.warning(request, "Your cart is empty.")
            return redirect("cart_summary")  

        
        for product in cart_items:
            quantity = quantities.get(str(product.id), 1)  
            Order.objects.create(
                product=product,
                profile=profile,
                quantity=quantity,
                address=address,
                phone=phone,
                date=timezone.now(),
                status=True  
            )

        cart.clear()

        messages.success(request, "Your order has been placed successfully!")
        return redirect("home")  

    return redirect("cart_summary") 
