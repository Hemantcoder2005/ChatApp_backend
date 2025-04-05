from django.urls import path,include
from .views import WarmMe
urlpatterns = [
   path("accounts/",include("accounts.urls")),
   path("friends/",include("friends_handler.urls")),
   path("warmme/", WarmMe)
]
