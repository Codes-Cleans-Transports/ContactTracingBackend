from django.shortcuts import render
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.serializers import IntegerField, DateTimeField, DictField, ListField
from .services import create_or_update_contact
from user.models import User, ContactsRel
from user.selectors import get_user, get_users_risk


# Create your views here.
class ContactCreateView(views.APIView):

    class InputSerializer(serializers.Serializer):
        mac = serializers.CharField(required=True)

    class OutputSerializer(serializers.Serializer):
        pass

    def post(self, request, mac):
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        contact = create_or_update_contact(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class ContactDetailView(views.APIView):

    class OutputSerializer(serializers.Serializer):
        risks = ListField()

    def get(self, request, mac):
        risks = get_users_risk(mac=mac, range=2)

        serializer = self.OutputSerializer({'risks': risks})

        return Response(data=serializer.data)
