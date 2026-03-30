from django.urls import path, include
from productions import views

app_name = 'productions'

productions_patterns = [
    path('', views.ProductionDetailView.as_view(), name='production_detail'),
    path('edit/', views.ProductionUpdateView.as_view(), name='production_edit'),
    path('delete/', views.ProductionDeleteView.as_view(), name='production_delete'),
]

category_patterns = [
    path('edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]

urlpatterns = [
    path('create/', views.ProductionCreateView.as_view(), name='production_create'),
    path('by_category/<slug:slug>/', views.ProductionByCategoryListView.as_view(), name='production_list_by_category'),
    path('production/<slug:slug>/', include(productions_patterns)),
    path('categories/', include([
            path('', views.CategoryListView.as_view(), name='category_list'),
            path('create/', views.CategoryCreateView.as_view(), name='category_create'),
            path('<slug:slug>/', include(category_patterns)),
        ]),
    ),
]