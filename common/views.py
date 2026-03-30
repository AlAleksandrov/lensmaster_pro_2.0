from django.shortcuts import render
from django.views.generic import TemplateView
from productions.models import Category, Production

# Create your views here
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.all().prefetch_related('productions')[:3]
        context['latest_productions'] = Production.objects.select_related('category').order_by('-created_at')[:3]
        return context


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)