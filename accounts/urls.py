from django.urls import path
from .views import CustomLoginView, CustomSignUpView, CatManagementView, CatCreateView, CatUpdateView, HealthDietListView, HealthDietCreateView, HealthDietUpdateView, HealthDietDeleteView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cat_management/', CatManagementView.as_view(), name='cat_management'),
    path('cats/add/', CatCreateView.as_view(), name='cat_add'),
    path('cats/<int:pk>/edit/', CatUpdateView.as_view(), name='cat_edit'),
    path('healthdiet/', HealthDietListView.as_view(), name='healthdiet_list'),
    path('healthdiet/add/', HealthDietCreateView.as_view(), name='healthdiet_add'),
    path('healthdiet/edit/<int:pk>/', HealthDietUpdateView.as_view(), name='healthdiet_edit'),
    path('healthdiet/delete/<int:pk>/', HealthDietDeleteView.as_view(), name='healthdiet_delete'),
]