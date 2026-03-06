from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from .models import Cart

class CartMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.create()

        request.cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
        return None