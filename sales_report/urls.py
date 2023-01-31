from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("my_api/", include("my_api.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
