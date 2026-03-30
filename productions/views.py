from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from productions.forms import ProductionForm, CategoryForm
from productions.models import Category, Production


# Create your views here.
class CategoryListView(ListView):
    model = Category
    template_name = 'productions/category_list.html'
    context_object_name = 'categories'
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()

        categories_on_page = context['page_obj']

        grouped_portfolio = []
        for category in categories_on_page:
            productions = Production.objects.filter(category=category)

            if q:
                productions = productions.filter(
                    Q(title__icontains=q)
                        |
                    Q(short_description__icontains=q)
                        |
                    Q(location__icontains=q)
                )

            if productions.exists():
                grouped_portfolio.append({
                    'category': category,
                    'items': productions,
                })

        context['grouped_portfolio'] = grouped_portfolio
        context['search_query'] = q
        context['production_create_url'] = reverse_lazy('productions:production_create')
        context['category_create_url'] = reverse_lazy('productions:category_create')
        return context

class ProductionByCategoryListView(ListView):
    model = Production
    template_name = 'productions/production_list.html'
    context_object_name = 'productions'
    paginate_by = 2

    def get_queryset(self):
        qs = Production.objects.filter(category__slug=self.kwargs['slug']).order_by('-created_at')
        q = self.request.GET.get('q', '').strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                    |
                Q(short_description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        except Category.DoesNotExist:
            context['category'] = None

        context['search_query'] = self.request.GET.get('q', '')

        return context


class ProductionDetailView(DetailView):
    model = Production
    template_name = 'productions/production_detail.html'
    context_object_name = 'production'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_productions'] = Production.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        )[:3]

        return context

class ProductionCreateView(CreateView):
    model = Production
    form_class = ProductionForm
    template_name = 'productions/production_form.html'
    success_url = reverse_lazy('productions:category_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class ProductionUpdateView(UpdateView):
    model = Production
    form_class = ProductionForm
    template_name = 'productions/production_form.html'
    success_url = reverse_lazy('productions:category_list')

class ProductionDeleteView(DeleteView):
    model = Production
    template_name = 'productions/production_confirm_delete.html'
    success_url = reverse_lazy('productions:category_list')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'productions/category_form.html'
    success_url = reverse_lazy('productions:category_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'productions/category_form.html'
    success_url = reverse_lazy('productions:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'productions/category_confirm_delete.html'
    success_url = reverse_lazy('productions:category_list')