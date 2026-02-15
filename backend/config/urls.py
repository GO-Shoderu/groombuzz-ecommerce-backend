# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import include, path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # JWT Auth
#     path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

#     # APIs
#     path("api/", include("catalog.urls")),
#     path("api/", include("transactions.urls")),
#     path("api/", include("engagement.urls")),
# ]

# from django.http import JsonResponse

# def health(request):
#     return JsonResponse({"status": "ok", "service": "GroomBuzz API"})

# urlpatterns = [
#     path("", health),
#     path("api/", include("accounts.urls")),
#     path("api/", include("catalog.urls")),
#     path("api/", include("transactions.urls")),
#     path("api/", include("engagement.urls")),
# ]

from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def health(request):
    return JsonResponse({"status": "ok", "service": "GroomBuzz API"})

urlpatterns = [
    # Root health check (so visiting the base URL doesn't look "broken")
    path("", health),

    # Admin
    path("admin/", admin.site.urls),

    # JWT Auth
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # APIs (I recommend giving each app its own prefix)
    path("api/accounts/", include("accounts.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/transactions/", include("transactions.urls")),
    path("api/engagement/", include("engagement.urls")),
]
