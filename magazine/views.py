from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Magazine
from .serializers import MagazineSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CreateMagazineView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to create a magazine."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = MagazineSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateMagazineView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, id):
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to update a magazine."}, status=status.HTTP_403_FORBIDDEN)
        magazine = get_object_or_404(Magazine, magazineId=id, writer=request.user)
        serializer = MagazineSerializer(magazine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveMagazineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        magazine = get_object_or_404(Magazine.objects.prefetch_related('imageFiles'), magazineId=id)
        serializer = MagazineSerializer(magazine, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteMagazineView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to delete a magazine."}, status=status.HTTP_403_FORBIDDEN)
        magazine = get_object_or_404(Magazine, magazineId=id, writer=request.user)
        magazine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListMagazineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        magazineList = Magazine.objects.prefetch_related('imageFiles').all()
        if not magazineList.exists():
            return Response({'detail': 'No magazines found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MagazineSerializer(magazineList, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RecentMagazinesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_magazines = Magazine.objects.prefetch_related('imageFiles').all().order_by('-createdAt')[:3]
        if not recent_magazines.exists():
            return Response({'detail': 'No recent magazines found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MagazineSerializer(recent_magazines, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)