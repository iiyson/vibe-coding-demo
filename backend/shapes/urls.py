from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShapeItemViewSet, LoginView, LogoutView, RegisterView

router = DefaultRouter()
router.register("items", ShapeItemViewSet, basename="shapeitem")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("auth/logout/", LogoutView.as_view(), name="api-logout"),
    path("auth/register/", RegisterView.as_view(), name="api-register"),
    path("", include(router.urls)),
]
