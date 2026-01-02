from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShapeItem
from .serializers import ShapeItemSerializer


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any authenticated user.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin or user.is_staff or user.is_superuser


class ShapeItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing shape items.
    """
    queryset = ShapeItem.objects.all()
    serializer_class = ShapeItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # Basic validation
        if not data.get("name") or not data.get("color") or not data.get("timestamp") or not data.get("shape_type"):
            return Response({"detail": "Name, color, shape type and timestamp are required"}, status=status.HTTP_400_BAD_REQUEST)
             
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class LoginView(APIView):
    """
    API View for user login. Returns a token and user info.
    """
    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "username": user.username,
            "is_admin": user.is_admin or user.is_staff or user.is_superuser,
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API View for user logout. Deletes the current token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        if token:
            token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    """
    API View for user registration.
    """
    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(username) > 150:
            return Response({"detail": "Username is too long"}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({"detail": "Password must be at least 6 characters"}, status=status.HTTP_400_BAD_REQUEST)
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, is_staff=False)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "username": user.username,
            "is_admin": user.is_admin or user.is_staff or user.is_superuser,
        }
        return Response(data, status=status.HTTP_201_CREATED)
