from django.contrib.auth import get_user_model
from rest_framework import viewsets

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer