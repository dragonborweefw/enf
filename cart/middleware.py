from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from .models import Cart

class CartMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.create()

        
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                
                if cart.session_key != request.session.session_key:
                    cart.session_key = request.session.session_key
                    cart.save()
                request.cart = cart
                return None
            except Cart.DoesNotExist:
                pass

        
        request.cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )

        request.session['cart_id'] = request.cart.id
        request.session.modified = True
        return None