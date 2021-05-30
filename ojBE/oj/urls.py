"""oj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (TokenRefreshView, )

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('account.urls.user_urls')),
    path('api/admin/', include('account.urls.admin_urls')),
    path('api/', include('problem.urls.user_urls')),
    path('api/admin/', include('problem.urls.admin_urls')),
    path('api/', include('submission.urls.user_urls')),
    path('api/', include('battle.urls.user_urls')),
]
