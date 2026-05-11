from .serializers import InvoiceSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Invoice

class InvoiceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Invoice.objects.all()
        return Invoice.objects.filter(user = user)