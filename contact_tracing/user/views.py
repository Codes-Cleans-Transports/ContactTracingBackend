from django.shortcuts import render
from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework import status

from .services import create_user

# Create your views here.


class UserCreateView(views.APIView):

    class InputSerializer(serializers.Serializer):
        mac = serializers.CharField(required=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()

    def post(self, request):
        
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)

        output_serializer = self.OutputSerializer({'id': user.id})

        return Response(data=output_serializer.data)

    
        



