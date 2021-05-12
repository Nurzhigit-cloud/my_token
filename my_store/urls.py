"""blog URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from products.views import CategoriesListView, ProductViewSet, ReviewCreateView, api_root

router = DefaultRouter()
router.register('products', ProductViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Product Api',
        default_version='v1',
        description='My product\'s Api'
    ), public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    path('', api_root),
    path('api/v1/categories/', CategoriesListView.as_view(), name='categories-list'),
    path('api/v1/review/', ReviewCreateView.as_view(), name='create-review'),
    # path('api/v1/cart/', CartProductView.as_view(), name='create-cart')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
