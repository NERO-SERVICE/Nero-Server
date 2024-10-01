from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Information
from .serializers import InformationSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CreateInformationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_product_writer:
            return Response({"detail": "You do not have permission to create a information."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = InformationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        information = get_object_or_404(Information.objects.prefetch_related('imageFiles'), infoId=id)
        serializer = InformationSerializer(information, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        informationList = Information.objects.prefetch_related('imageFiles').all()
        if not informationList.exists():
            return Response({'detail': 'No informations found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = InformationSerializer(informationList, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RecentInformationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_informations = Information.objects.prefetch_related('imageFiles').all().order_by('-createdAt')[:4]
        if not recent_informations.exists():
            return Response({'detail': 'No recent informations found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InformationSerializer(recent_informations, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
