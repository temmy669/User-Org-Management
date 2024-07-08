# from django.shortcuts import render
# from django.contrib.auth import authenticate
# from rest_framework import generics, status, viewsets
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import User, Organisation
# from .serializers import UserSerializer, OrganisationSerializer, LoginSerializer

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "status": "success",
#                 "message": "Registration successful",
#                 "data": {
#                     "accessToken": str(refresh.access_token),
#                     "user": UserSerializer(user).data
#                 }
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "status": "Bad request",
#             "message": "Registration unsuccessful",
#             "statusCode": 422,
#             "errors": serializer.errors
#         }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "status": "success",
#                 "message": "Login successful",
#                 "data": {
#                     "accessToken": str(refresh.access_token),
#                     "user": UserSerializer(user).data
#                 }
#             }, status=status.HTTP_200_OK)
#         return Response({
#             "status": "Bad request",
#             "message": "Authentication failed",
#             "statusCode": 401
#         }, status=status.HTTP_401_UNAUTHORIZED)

# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return User.objects.filter(id=user.id)

# class OrganisationViewSet(viewsets.ModelViewSet):
#     serializer_class = OrganisationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return user.organisations.all()

#     def perform_create(self, serializer):
#         serializer.save(users=[self.request.user])

# class OrganisationDetailView(generics.RetrieveAPIView):
#     queryset = Organisation.objects.all()
#     serializer_class = OrganisationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Organisation.objects.filter(users=user)

# class AddUserToOrganisationView(generics.GenericAPIView):
#     queryset = Organisation.objects.all()
#     serializer_class = OrganisationSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, orgId):
#         try:
#             organisation = Organisation.objects.get(id=orgId)
#         except Organisation.DoesNotExist:
#             return Response({
#                 "status": "Bad request",
#                 "message": "Organisation not found",
#                 "statusCode": 404
#             }, status=status.HTTP_404_NOT_FOUND)

#         userId = request.data.get('userId')
#         try:
#             user = User.objects.get(id=userId)
#         except User.DoesNotExist:
#             return Response({
#                 "status": "Bad request",
#                 "message": "User not found",
#                 "statusCode": 404
#             }, status=status.HTTP_404_NOT_FOUND)

#         organisation.users.add(user)
#         return Response({
#             "status": "success",
#             "message": "User added to organisation successfully"
#         }, status=status.HTTP_200_OK)



from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 422,
            "errors": serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'userId' 
class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.organisations.all()

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])

class OrganisationDetailView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Organisation.objects.filter(users=user)

class AddUserToOrganisationView(generics.GenericAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId):
        try:
            organisation = Organisation.objects.get(id=orgId)
        except Organisation.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "Organisation not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)

        userId = request.data.get('userId')
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "User not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)

        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully"
        }, status=status.HTTP_200_OK)
