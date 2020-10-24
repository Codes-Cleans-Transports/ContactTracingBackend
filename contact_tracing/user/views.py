from django.shortcuts import render
from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework import status

from .services import process_get_or_create_user
from .selectors import get_user

from .services import mark_positive

# Create your views here.


class UserDetailsView(views.APIView):

    class OutputSerializer(serializers.Serializer):
        status = serializers.CharField()
    
    def get(self, request, mac):
        
        user = process_get_or_create_user(mac=mac)

        output_serializer = self.OutputSerializer({'status': user.status})

        return Response(data=output_serializer.data)


class UserSetPositiveView(views.APIView):

    def put(self, request, mac):

        user = get_user(mac=mac)

        mark_positive(user)        

        return Response()







    
        



