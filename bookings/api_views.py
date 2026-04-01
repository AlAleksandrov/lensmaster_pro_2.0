from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from bookings.models import ServicePackage, BookingRequest
from bookings.serializers import ServicePackageSerializer, BookingRequestSerializer


class ServicePackageListAPIView(ListAPIView):
    queryset = ServicePackage.objects.filter(is_active=True)
    serializer_class = ServicePackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServicePackageDetailAPIView(RetrieveAPIView):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingRequestCreateAPIView(CreateAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated]