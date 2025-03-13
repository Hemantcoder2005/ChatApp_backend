from django.urls import path,include

urlpatterns = [
   path("accounts/",include("accounts.urls")),
   path("friends/",include("friends_handler.urls"))
]
