from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from inventory.forms import EquipmentForm
from inventory.models import Equipment


# Create your views here.
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'inventory/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 6

    def get_queryset(self):
        return Equipment.objects.filter(is_active=True).prefetch_related('productions').order_by('equipment_type', 'brand', 'model')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['productions'] = self.object.productions.all().select_related('category')

        return context


class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'inventory/equipment_form.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'inventory/equipment_form.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'inventory/equipment_confirm_delete.html'
    success_url = reverse_lazy('inventory:equipment_list')


class EquipmentByTypeListView(ListView):
    model = Equipment
    template_name = 'inventory/equipment_list_by_type.html'
    context_object_name = 'equipment_list'
    paginate_by = 2

    def get_queryset(self):
        self.equipment_type = self.kwargs['equipment_type']
        return Equipment.objects.filter(
            equipment_type=self.equipment_type,
            is_active=True
        ).order_by('brand', 'model')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.equipment_type

        for val, label in Equipment.EquipmentType.choices:
            if val == self.equipment_type:
                context['type_label'] = label
                break
        return context

