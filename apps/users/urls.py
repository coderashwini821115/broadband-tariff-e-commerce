from rest_framework.routers import DefaultRouter
from .views import LogoutViewSet, UserViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename = 'users')

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name = 'auth_register'),
    path('login/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('logout/', LogoutViewSet.as_view(), name= 'auth_logout'),
    path('me/', UserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'}), name = 'auth_me'),


]

urlpatterns += router.urls
