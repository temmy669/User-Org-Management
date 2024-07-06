from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserDetailView, OrganisationViewSet, OrganisationDetailView, AddUserToOrganisationView

router = DefaultRouter()
router.register(r'organisations', OrganisationViewSet, basename='organisation')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/', include(router.urls)),
    path('api/organisations/<int:orgId>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/<int:orgId>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
