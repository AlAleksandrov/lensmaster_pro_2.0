from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from bookings.filters import BookingRequestFilter, ServicePackageFilter
from bookings.models import ServicePackage, BookingRequest
from bookings.serializers import ServicePackageSerializer, BookingRequestSerializer


class ServicePackageListAPIView(ListAPIView):
    queryset = ServicePackage.objects.filter(is_active=True)
    serializer_class = ServicePackageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServicePackageFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration_hours']
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServicePackageDetailAPIView(RetrieveAPIView):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingRequestCreateAPIView(CreateAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [IsAuthenticated]


class BookingRequestListAPIView(ListAPIView):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BookingRequestFilter
    search_fields = ['first_name', 'last_name', 'email']
    permission_classes = [IsAuthenticated]
