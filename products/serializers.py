from rest_framework import serializers

from products.models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'image')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('slug')
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['category'] = CategorySerializer(instance.category, context=self.context).data
        representation['review'] = ReviewSerializer(instance.review.all(), many=True).data
        return representation


class ProductListSerializer(serializers.ModelSerializer):

    details = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'image', 'created_at', 'details']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['text', 'product', 'user', 'rating', 'created_at']

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Укажите рейтинг от 1 до 5')
        return rating

    def create(self, validated_data):
        requests = self.context.get('request')
        user = requests.user
        review = Review.objects.create(user=user, **validated_data)
        return review