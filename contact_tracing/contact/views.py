from django.shortcuts import render
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.serializers import IntegerField, DateTimeField, DictField, ListField
from .services import process_create_or_update_contacts
from user.models import User, ContactsRel
from user.selectors import get_user, get_users_risk, get_user_conections
from user.services import process_get_or_create_user


# Create your views here.
class ContactCreateDetailView(views.APIView):

    class OutputSerializer(serializers.Serializer):
        root = ListField()
        nodes = ListField()
        edges = ListField()
        duration = ListField()

    class InputSerializer(serializers.Serializer):
        macs = serializers.ListField(child=serializers.CharField())

    def post(self, request, mac):

        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = process_get_or_create_user(mac=mac)

        contact = process_create_or_update_contacts(user=user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, mac):
        user = get_user(mac=mac)
        duration = []
        root = []
        root.append(mac)

        user_risk = get_users_risk(mac=mac, range=4)
        user_conns = get_user_conections()[0]

        for contact in user.contacts.all():
            duration.append(user.contacts.relationship(contact).durations)

        serializer = self.OutputSerializer({'root':root,'nodes': user_risk, 'edges':user_conns, 'duration': duration})

        return Response(data=serializer.data)
