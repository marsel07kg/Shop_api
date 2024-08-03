from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ReviewProductSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer


# HOMEWORK №4


# @api_view(http_method_names=['GET', 'POST'])
# def category_list_api_view(request):
#     if request.method == 'GET':
#         category = Category.objects.all()
#         data = CategorySerializer(category, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#
#         name = request.data.get('name')
#
#         category = Category.objects.create(
#             name=name
#         )
#         return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})
#
#
# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = CategorySerializer(category, many=False).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         category.name = request.data.get('name')
#         category.save()
#         return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def products_list_api_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         data = ProductSerializer(products, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         # serializer = ProductValidateSerializer(data=request.data)
#         # if not serializer.is_valid():
#         #     return Response(status=status.HTTP_400_BAD_REQUEST,
#         #                     data=serializer.errors)
#
#         title = request.data.get('title')
#         description = request.data.get('description')
#         price = request.data.get('price')
#         tags = request.data.get('tags')
#         category_id = request.data.get('category_id')
#         category = Category.objects.get(id=category_id)
#
#         product = Product.objects.create(
#             title=title,
#             description=description,
#             price=price,
#             category=category
#         )
#
#         product.tags.set(tags)
#         product.save()
#         print(product)
#
#         return Response(status=status.HTTP_201_CREATED,
#                         data={'product_id': product.id})
#
#
# @api_view(http_method_names=['GET', 'POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         review = Review.objects.all()
#         data = ReviewSerializer(review, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#
#         text = request.data.get('text')
#         stars = request.data.get('stars')
#         product_id = request.data.get('product_id')
#         review_product = Product.objects.get(id=product_id)
#
#         review = Review.objects.create(
#             text=text,
#             stars=stars,
#             review_product=review_product
#
#         )
#         print(review)
#         return Response(status=status.HTTP_201_CREATED, data={'review_id': review.id})
#
#
# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewSerializer(review, many=False).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         review.text = request.data.get('text')
#         review.stars = request.data.get('stars')
#         review.product_id = request.data.get('product_id')
#         review.save()
#         return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(http_method_names=['GET'])
# def rev_product_list_api_view(request):
#     rev_products = Review.objects.all()
#     data = ReviewProductSerializer(rev_products, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)


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