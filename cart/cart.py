from store.models import Product, Profile


class Cart():
        def __init__(self, request):
            self.session = request.session
            # Get request
            self.request = request
            # Get the current session key if it exists
            cart = self.session.get('session_key')

            # If the user is new, no session key!  Create one!
            if 'session_key' not in request.session:
                cart = self.session['session_key'] = {}


            # Make sure cart is available on all pages of site
            self.cart = cart
            
            
        def add(self, product, quantity):
            product_id = str(product.id)
            product_qty = str(quantity)
            # Logic
            if product_id in self.cart:
                pass
            else:
                #self.cart[product_id] = {'price': str(product.price)}
                self.cart[product_id] = int(product_qty)

            self.session.modified = True
            
        def __len__(self):
            return len(self.cart)

        def get_prods(self):
            # Get ids from cart
            product_ids = self.cart.keys()
            # Use ids to lookup products in database model
            products = Product.objects.filter(id__in=product_ids)

            # Return those looked up products
            return products
            
        def get_quants(self):
                quantities = self.cart
                return quantities   
            
        def delete(self, product):
            product_id = str(product)
            # Delete from dictionary/cart
            if product_id in self.cart:
                del self.cart[product_id]

            self.session.modified = True

            # # Deal with logged in user
            # if self.request.user.is_authenticated:
            #     # Get the current user profile
            #     current_user = Profile.objects.filter(user__id=self.request.user.id)
            #     # Convert {'3':1, '2':4} to {"3":1, "2":4}
            #     carty = str(self.cart)
            #     carty = carty.replace("\'", "\"")
            #     # Save carty to the Profile Model
            #     current_user.update(old_cart=str(carty))
        def save(self):
            self.session["cart"] = self.cart
            self.session.modified = True
        
        def clear(self):
            self.cart.clear()  
            self.save()
            
        
        