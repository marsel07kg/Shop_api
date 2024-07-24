from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']

    def get_product_count(self, category):
        count = category.categories.count()
        return count


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'description', 'price', 'category']
        depth = 1

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review', 'text', 'stars']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id description price'.split()


class ReviewProductSerializer(serializers.ModelSerializer):
    review_product = ProductReviewSerializer()

    class Meta:
        model = Review
        fields = ['id', 'review_product', 'text', 'stars', 'rating_stars']


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=50)
    description = serializers.CharField(min_length=1, max_length=100, required=False)
    price = serializers.IntegerField(min_value=1)
    category = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    review_product = serializers.IntegerField()