from django.urls import include, path

urlpatterns = [
    path("v1/", include("authentication.v1.urls")),
]
