from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminRole
from .serializers import RegisterSerializer, LogoutSerializer, UserSerializer

CustomUser = get_user_model()
class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer
        
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        
        if self.action == 'me':
            return [IsAuthenticated()]
        
        return [IsAdminRole()]

    @action(detail = False, methods = ['get', 'put', 'patch'])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data = request.data, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
class LogoutViewSet(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post (self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(status = status.HTTP_205_RESET_CONTENT)
