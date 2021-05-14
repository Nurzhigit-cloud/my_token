from rest_framework import viewsets

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.permissions import IsAuthorPermission, IsAdminPermission



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    with_items = CartItem
    permission_classes = [IsAuthorPermission] or [IsAdminPermission]
    def get_queryset(self):
        qs = self.request.user
        queryset = super().get_queryset()
        if qs.is_anonymous:
            return ''
        queryset = queryset.filter(user=qs)
        return queryset
