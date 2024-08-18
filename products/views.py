from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import DrfProduct
from .serializers import DrfProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import logging

logger = logging.getLogger('django')


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        logger.debug("Request data: %s", request.data)
        
        serializer = DrfProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("Serializer errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, id):
        product = get_object_or_404(DrfProduct, id=id, owner=request.user) 
        serializer = DrfProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 제품 조회
class RetrieveProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        product = get_object_or_404(DrfProduct, id=id, owner=request.user)  # 유저가 소유한 제품인지 확인
        serializer = DrfProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# 제품 삭제
class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        product = get_object_or_404(DrfProduct, id=id, owner=request.user)  # 유저가 소유한 제품인지 확인
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 사용자가 소유한 모든 제품 리스트 조회
class ListProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 요청한 사용자의 모든 제품을 필터링합니다.
        products = DrfProduct.objects.filter(owner=request.user)
        
        if not products.exists():
            return Response({'detail': 'No products found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DrfProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)