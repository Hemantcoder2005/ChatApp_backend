from django.urls import path,include
from .views import sendRequest,removeRequest,RequestManager,FriendManager
urlpatterns = [
    path("manageRequest",RequestManager.as_view(),name="requestManager"),
    path("manageFriends",FriendManager.as_view(),name="manageFriend"),
]
