from accounts import views
from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('profile/', include([
        path('',views.ProfileDetailView.as_view(), name='profile_detail'),
        path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    ])),
]