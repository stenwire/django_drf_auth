from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authme.serializers import UserDetailsSerializer


class GreetingView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        response = {}
        response["status"] = status.HTTP_200_OK
        response["greeting"] = "Hello World 🤗"
        return Response(response)


class UserDetailsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data)
