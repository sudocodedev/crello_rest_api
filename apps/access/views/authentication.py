from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.common.views import (
    NonAuthenticatedAPIMixin,
    AppAPIView,
)
from apps.access.serializers import (
    UserLoginResponseSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserInfoSerializer,
)
from apps.common.views.generic import (
    AppModelCUDAPIViewSet,
    AppModelListAPIViewSet,
)

User = get_user_model()


class MEAPIView(AppAPIView):
    serializer_class = UserInfoSerializer

    def get(self, *args, **kwargs):
        user = self.get_authenticated_user()
        if user:
            serializer = UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        return self.send_error_response('User not authenticated')

    def put(self, request, *args, **kwargs):
        modification= request.data
        user = self.get_user()
        serializer = UserInfoSerializer(user, data=modification)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        modification = request.data
        user = self.get_user()
        serializer = UserInfoSerializer(user, data=modification, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        user = self.get_user()
        user.delete()
        return Response({'detail':"user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserViewset(AppModelListAPIViewSet):
    queryset = User.objects.all().order_by("-created")
    serializer_class = UserInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(AppAPIView):
    def post(self, *args, **kwargs):
        user = self.get_authenticated_user()
        if user:
            Token.objects.filter(user=user).delete()
            return self.send_response("user logged out")
        return self.send_error_response('Trouble in logging out')
    

class SignUpAPIView(NonAuthenticatedAPIMixin, AppAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_valid_serializer()
        serializer.save()
        return self.send_response(data="user signed up successfullly", status_code=status.HTTP_201_CREATED)
    
class LoginAPIView(NonAuthenticatedAPIMixin, AppAPIView):
    serializer_class = UserLoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_valid_serializer()
        user = serializer.validated_data['user']
        return self.send_response(
            data=UserLoginResponseSerializer(user).data,
        )
    
class RefreshTokenAPIView(AppAPIView):
    def get(self, *args, **kwargs):
        user = self.get_user()

        if user:
            return self.send_response(
                data=UserLoginResponseSerializer(user).data,
            )