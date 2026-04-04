from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from common.mixins import PhotographerRequiredMixin
from inventory.forms import EquipmentForm
from inventory.models import Equipment


# Create your views here.
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'inventory/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 6

    def get_queryset(self):
        qs = Equipment.objects.prefetch_related('productions').order_by('equipment_type', 'brand', 'model')
        user = getattr(self.request, 'user', None)
        is_photographer = False
        if user:
            is_photographer = getattr(user, 'is_authenticated', False) and (getattr(user, 'is_superuser', False) or user.groups.filter(name='Photographers').exists())
        if not is_photographer:
            qs = qs.filter(is_active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_items = context['page_obj']

        types = Equipment.EquipmentType.choices

        grouped = []
        for val, label in types:
            items_in_group = [item for item in page_items if item.equipment_type == val]
            if items_in_group:
                grouped.append({
                    'type': label,
                    'type_val': val,
                    'items': items_in_group,
                })

        context['grouped_equipment'] = grouped

        return context


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'inventory/equipment_detail.html'
    context_object_name = 'item'

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        user = self.request.user
        is_photographer = user.is_authenticated and (user.is_superuser or user.groups.filter(name='Photographers').exists())
        if not obj.is_active and not is_photographer:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['productions'] = self.object.productions.all().select_related('category')

        return context


class EquipmentCreateView(PhotographerRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'inventory/equipment_form.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentUpdateView(PhotographerRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'inventory/equipment_form.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentDeleteView(PhotographerRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'inventory/equipment_confirm_delete.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentByTypeListView(ListView):
    model = Equipment
    template_name = 'inventory/equipment_list_by_type.html'
    context_object_name = 'equipment_list'
    paginate_by = 2

    def get_queryset(self):
        qs = Equipment.objects.filter(equipment_type=self.kwargs['equipment_type'])
        user = self.request.user
        is_photographer = user.is_authenticated and (user.is_superuser or user.groups.filter(name='Photographers').exists())
        if not is_photographer:
            qs = qs.filter(is_active=True)
        return qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_type = self.kwargs.get('equipment_type')
        context['current_type'] = equipment_type

        for val, label in Equipment.EquipmentType.choices:
            if val == equipment_type:
                context['type_label'] = label
                break
        return context


class ToggleFavoriteEquipmentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        equipment = get_object_or_404(Equipment, pk=pk)
        profile = request.user.profile

        if equipment in profile.favorite_equipment.all():
            profile.favorite_equipment.remove(equipment)
        else:
            profile.favorite_equipment.add(equipment)

        return redirect('inventory:equipment_detail', pk=pk)