
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ReviewProductSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer


@api_view(http_method_names=['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category = Category.objects.all()
        data = CategorySerializer(category, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get['title']
        description = serializer.validated_data.get['description']
        price = serializer.validated_data.get['price']
        category_id = serializer.validated_data.get['category']
        tags = serializer.validated_data.get['tags']

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        product.tags.set(tags)
        product.save()

        return Response(status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(review, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')
        review_product = Product.objects.get(id=product_id)

        review = Review.objects.create(
            text=text,
            stars=stars,
            review_product=review_product

        )
        print(review)
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
def rev_product_list_api_view(request):
    rev_products = Review.objects.all()
    data = ReviewProductSerializer(rev_products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)