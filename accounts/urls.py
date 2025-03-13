from django.urls import path,include
from .views import CustomUserCreateView,CustomTokenObtainPairView,GetUserDetails
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    )
urlpatterns = [
    path("signup/",CustomUserCreateView.as_view(),name="signup"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("getUser/",GetUserDetails.as_view(),name="user-details"),
]
