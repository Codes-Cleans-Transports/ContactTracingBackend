from django.shortcuts import render
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.serializers import IntegerField, DateTimeField, DictField
from .services import create_or_update_contact
from user.models import User, ContactsRel
from user.selectors import get_user


# Create your views here.
class ContactCreateView(views.APIView):

    class InputSerializer(serializers.Serializer):
        mac1 = serializers.CharField(required=True)
        mac2 = serializers.CharField(required=True)

    class OutputSerializer(serializers.Serializer):
        pass

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        contact = create_or_update_contact(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class ContactsDetailView(views.APIView):

    class OutputSerializer(serializers.Serializer):
        contacts = DictField()

    def get(self, request, mac):
        user = get_user(mac=mac)
        import pdb;pdb.set_trace()

        serializer = self.OutputSerializer({'contacts':user.nodes.all()})

        return Response(data=serializer.data)
