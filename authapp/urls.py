from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserDetailView, OrganisationViewSet, OrganisationDetailView, AddUserToOrganisationView

router = DefaultRouter()
router.register(r'organisations', OrganisationViewSet, basename='organisation')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    # path('api/users/<str:userId>/', UserDetailView.as_view(), name='user-detail'),
    # path('api/', include(router.urls)),
    # path('api/organisations/<str:orgId>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    # path('api/organisations/<str:orgId>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
