from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from bookings.forms import BookingRequestForm, ServicePackageForm
from bookings.models import BookingRequest, ServicePackage
from django.db.models import Q
from common.mixins import PhotographerRequiredMixin
from productions.models import Category


# Create your views here.
class BookingCreateView(CreateView):
    model = BookingRequest
    form_class = BookingRequestForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_success')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email

            try:
                if hasattr(user, 'profile'):
                    initial['phone'] = user.profile.phone
                    initial['city'] = user.profile.city
            except Exception:
                pass
        return initial


    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        package_id = self.request.GET.get('package')
        if package_id:
            form.fields['package'].initial = package_id
        return form


class BookingListView(PhotographerRequiredMixin, ListView):
    model = BookingRequest
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status', '').strip()
        q = self.request.GET.get('q', '').strip()

        if status:
            qs = qs.filter(status=status)

        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                    |
                Q(last_name__icontains=q)
                    |
                Q(email__icontains=q)
                    |
                Q(phone__icontains=q)

            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = BookingRequest.Status.choices
        context['current_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class BookingUpdateView(PhotographerRequiredMixin, UpdateView):
    model = BookingRequest
    fields = ['status', 'internal_notes', 'event_date', 'package']
    template_name = 'bookings/booking_edit.html'
    success_url = reverse_lazy('bookings:booking_list')


class BookingDeleteView(PhotographerRequiredMixin, DeleteView):
    model = BookingRequest
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:booking_list')


class ServicePackageListView(ListView):
    model = ServicePackage
    template_name = 'bookings/package_list.html'
    context_object_name = 'packages'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('category__name', 'price')

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['package_create_url'] = reverse_lazy('bookings:package_create')
        return context


class ServicePackageDetailView(DetailView):
    model = ServicePackage
    template_name = 'bookings/package_detail.html'
    context_object_name = 'package'


class ServicePackageCreateView(PhotographerRequiredMixin, CreateView):
    model = ServicePackage
    form_class = ServicePackageForm
    template_name = 'bookings/package_form.html'
    success_url = reverse_lazy('bookings:package_list')


class ServicePackageUpdateView(PhotographerRequiredMixin, UpdateView):
    model = ServicePackage
    form_class = ServicePackageForm
    template_name = 'bookings/package_form.html'
    success_url = reverse_lazy('bookings:package_list')


class ServicePackageDeleteView(PhotographerRequiredMixin, DeleteView):
    model = ServicePackage
    template_name = 'bookings/package_confirm_delete.html'
    success_url = reverse_lazy('bookings:package_list')


class ServicePackageByCategoryListView(ListView):
    model = ServicePackage
    template_name = 'bookings/package_list_by_category.html'
    context_object_name = 'packages'
    paginate_by = 2

    def get_queryset(self):
        return ServicePackage.objects.filter(category_id=self.kwargs['category_id']).order_by('price')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = Category.objects.get(pk=self.kwargs['category_id']).name
        return context


class ToggleFavoritePackageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        package = get_object_or_404(ServicePackage, pk=pk)
        profile = request.user.profile

        if package in profile.favorite_packages.all():
            profile.favorite_packages.remove(package)
        else:
            profile.favorite_packages.add(package)

        return redirect('bookings:package_detail', pk=pk)
