from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from chat.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


# here for permission added because otherwise everyone can access the api
@permission_classes(IsAuthenticated)
@api_view(["GET"])
def getuser_list(request):
    try:
        user_obj = User.objects.exclude(id=request.user.id)
        serializer = UserSerializer(user_obj, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print("error in getting user list", str(e))
        return Response({"error": "Error in getting users list"}, status=400)
