from django.shortcuts import render
from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework import status

from .services import process_get_or_create_user
from .selectors import get_user, get_users_risk

from .services import mark_positive

# Create your views here.


class UserDetailsPatchView(views.APIView):

    class OutputSerializer(serializers.Serializer):
        status = serializers.CharField()
        safety = serializers.CharField()

    
    def get(self, request, mac):
        
        user = process_get_or_create_user(mac=mac)
        users_risk = get_users_risk(mac=mac, range=2)

        output_serializer = self.OutputSerializer({'status': user.status, 'safety': user.safety})

        return Response(data=output_serializer.data)


    def put(self, request, mac):

        user = get_user(mac=mac)

        mark_positive(user)        

        return Response()

    








    
        



