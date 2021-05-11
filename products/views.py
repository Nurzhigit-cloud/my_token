from django.shortcuts import render
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from products.models import Category, Product, Review, Basket
from products.permissions import IsAdminPermission, IsAuthorPermission
from products.serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductListSerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['slug', 'price']
    search_fields = ['title', 'description', 'active']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    @action(['GET'], detail=True)
    def review(self, request, slug=None):
        product = self.get_object()
        reviews = product.review.all()
        serializers = ReviewSerializer(reviews, many=True)
        return Response(serializers.data)


    @action(['POST'], detail=True)
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        try:
            basket = Basket.objects.get(post=post, user=user)
            basket.is_liked = not basket.is_liked
            basket.save()
            message = 'liked' if basket.is_liked else 'dislike'
        except Basket.DoesNotExist:
            Basket.objects.create(post=post, user=user, is_liked=True)
        return Response(message, status=200)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        elif self.action in ['basket', 'review']:
            permissions = [IsAuthenticated] or [IsAdminPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
        'categories': reverse('categories-list', request=request, format=format),
    })


class ReviewCreateView(CreateView):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]

