from dj_rest_auth.registration.views import RegisterView
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from project_app.serializers import CustomRegisterSerializer

# Create your views here.
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        try:
            return super().perform_create(serializer)
        except IntegrityError:
            raise ValidationError({"email": ["A user is already registered with this email address."]})