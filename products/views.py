from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import DrfProduct
from .serializers import DrfProductSerializer

# 생성
class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DrfProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 검색
class RetrieveProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        product = get_object_or_404(DrfProduct, doc_id=doc_id)
        serializer = DrfProductSerializer(product)
        return Response(serializer.data)

# 수정
class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, doc_id):
        product = get_object_or_404(DrfProduct, doc_id=doc_id)
        if product.owner != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = DrfProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 삭제
class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        product = get_object_or_404(DrfProduct, doc_id=doc_id)
        if product.owner != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 리스트 불러오기
class ListProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = DrfProduct.objects.all()
        serializer = DrfProductSerializer(products, many=True)
        return Response(serializer.data)
