from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import DrfProduct
from .serializers import DrfProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import logging


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # 사용자가 로그인했는지 확인
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # 제품 작성 권한이 있는지 확인
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to create a product."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DrfProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, id):
        
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to update a product."}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(DrfProduct, productId=id, writer=request.user)
        serializer = DrfProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 제품 조회
class RetrieveProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        product = get_object_or_404(DrfProduct, productId=id)  # writer 조건 제거
        serializer = DrfProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# 제품 삭제
class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        # 제품 작성 권한이 있는지 확인
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to delete a product."}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(DrfProduct, productId=id, writer=request.user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 사용자가 소유한 모든 제품 리스트 조회
class ListProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 모든 사용자의 제품을 조회
        products = DrfProduct.objects.all()

        if not products.exists():
            return Response({'detail': 'No products found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DrfProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)