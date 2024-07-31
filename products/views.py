from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ReviewProductSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def post(self, request, *args, **kwargs):
        validator = ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})

        title = validator.validated_data['title']
        description = validator.validated_data['description']
        price = validator.validated_data['price']
        category_id = validator.validated_data['category']
        tags = validator.validated_data['tags']

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )

        product.tags.set(tags)
        product.save()

        return Response(status=status.HTTP_201_CREATED)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        product_detail = self.get_object()
        validator = ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})

        product_detail.title = validator.validated_data['title']
        product_detail.description = validator.validated_data['description']
        product_detail.price = validator.validated_data['price']
        product_detail.category_id = validator.validated_data['category']
        product_detail.tags.set(validator.validated_data['tags'])
        product_detail.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product_detail = Product.objects.get(id=id)
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        validator = ReviewValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})
        print(request.data)

        text = validator.validated_data['text']
        product_id = validator.validated_data['product']
        stars = validator.validated_data['stars']
        Review.objects.create(
            product_id=product_id,
            stars=stars,
            text=text
        )

        return Response(status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        review_detail = self.get_object()
        validator = ReviewValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})

        review_detail.text = validator.validated_data['text']
        review_detail.product_id = validator.validated_data['product']
        review_detail.stars = validator.validated_data['stars']
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        review_detail = self.get_object()
        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)