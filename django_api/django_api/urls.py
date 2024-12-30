from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from snippets import views
from oauth2_provider import urls as oauth2_urls

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include(oauth2_urls)),
    path('', include('snippets.urls')),
]