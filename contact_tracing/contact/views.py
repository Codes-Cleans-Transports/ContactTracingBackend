from django.shortcuts import render
from rest_framework import serializers, views, response
from .services import create_contact

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

        contact = create_contact(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
