from rest_framework import serializers, exceptions

from products.models import Product
from products.serializers import ProductSerializer
from .models import Cart, CartItem


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', )
    product = ProductSerializer()


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True, write_only=True)
    quantity = serializers.IntegerField(default=1)
    product = ProductSerializer(read_only=True)


class CartItemsSerializer(serializers.Serializer):
    products = serializers.ListField(child=CartItemSerializer())

    product_id = serializers.IntegerField(required=True, write_only=True)
    quantity = serializers.IntegerField(default=1)
    product = ProductSerializer(read_only=True)
    def create(self, validated_data):
        """Add desserts to cart."""
        # Get current user
        user = self.context['request'].user

        # Get current car items
        current_cart = CartItem.objects.filter(owner=user)
        current_cart_items_ids = map(lambda item: item.dessert_id, current_cart)

        # List to prepare items in-memory for bulk save
        cart_items = list()

        for product_data in validated_data['product']:
            product_id = product_data['product_id']
            # Break and return 400 if a dessert already in cart
            if product_id in current_cart_items_ids:
                raise exceptions.ParseError(detail="Dessert (%s) alraedy exists in the cart" % product_id)
                return
            try:  # Check if item_id added to cart is valid dessert_id else return 400
                product = Product.objects.get(id=product_id)  # FIXME: Bulk query instead of looping
            except Product.DoesNotExist:
                raise exceptions.ParseError(detail="No such Dessert ID (%s)" % product_id)
                return

            # Create CartItem in memory and add to cart_items list
            quantity = product_data['quantity']
            cart_items.append(
                CartItem(owner=user, product=product, quantity=quantity)
            )

        # Bulk save cart_items to DB
        result = CartItem.objects.bulk_create(cart_items)

        # Merge recently added items with the current ones in 'shared_with'cart to resturn
        # response with all items in cart
        response = {'desserts': list(current_cart) + result}
        return response






















#
# class CartSerializer(serializers.ModelSerializer):
#      items = CartItemSerializer(many=True)
#     total_price = serializers.ReadOnlyField(source='get_total_price')
#
#     class Meta:
#         model = Cart
#         fields = ('id', 'items', 'total_price')
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         items = validated_data.pop('items')
#         user = request.user
#         cart = Cart.objects.create(user=user)
#         for item in items:
#             print(item)
#             CartItem.objects.create(cart=cart,
#                                     product=item['product'],
#                                     amount=item['amount'])
#         cart.save()
#         return cart
#
#     def to_representation(self, instance):
#         representation = super(CartSerializer, self).to_representation(instance)
#         representation['user'] = instance.user.email
#         representation['products'] = CartItemSerializer(instance.cartitem.all(), many=True).data
#         return representation
