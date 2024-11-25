from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, FamilyMember, Token
from .serializers import UserSerializer, FamilyMemberSerializer, TokenSerializer
from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate
from .backends import authenticate
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        print(f"Registering user with email: {email}")
        if User.objects.filter(email=email).exists():
            return Response({"error": "This email is already registered"}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        print(f"User created: {user}")
        token = Token.objects.create(user=user)
        print(f"Token created: {token.key}")
        return Response({"access_token": token.key, "refresh_token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Logging in user with email: {email}")
        user = authenticate(request=request, username=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(f"Token: {token.key}, Created: {created}")
            return Response({"access_token": token.key, "refresh_token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class AddFamilyMemberView(APIView):
    def authenticate_request(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None, "No token provided"

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'token':
                return None, "Invalid token format"
        except ValueError:
            return None, "Invalid token format"

        try:
            token_obj = Token.objects.get(key=token)
            print(f"Token found: {token_obj.key}")
            return token_obj.user, None
        except Token.DoesNotExist:
            print(f"Token not found: {token}")
            return None, "Invalid token"

    def has_permission(self, request):
        user, error = self.authenticate_request(request)
        if user:
            request.user = user
            return True
        return False

    def post(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name')
        surname = request.data.get('surname')
        age = request.data.get('age')
        gender = request.data.get('gender')

        user = request.user
        print(f"Adding family member for user: {user}")

        family_member = FamilyMember.objects.create(
            user=user,
            name=name,
            surname=surname,
            age=age,
            gender=gender
        )
        return Response({"message": "Family member added successfully"}, status=status.HTTP_201_CREATED)

class ListFamilyMembersView(APIView):
    def authenticate_request(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None, "No token provided"

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'token':
                return None, "Invalid token format"
        except ValueError:
            return None, "Invalid token format"

        try:
            token_obj = Token.objects.get(key=token)
            print(f"Token found: {token_obj.key}")
            return token_obj.user, None
        except Token.DoesNotExist:
            print(f"Token not found: {token}")
            return None, "Invalid token"

    def has_permission(self, request):
        user, error = self.authenticate_request(request)
        if user:
            request.user = user
            return True
        return False

    def get(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        family_members = FamilyMember.objects.filter(user=user)
        serializer = FamilyMemberSerializer(family_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def authenticate_request(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None, "No token provided"

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'token':
                return None, "Invalid token format"
        except ValueError:
            return None, "Invalid token format"

        try:
            token_obj = Token.objects.get(key=token)
            print(f"Token found: {token_obj.key}")
            return token_obj.user, None
        except Token.DoesNotExist:
            print(f"Token not found: {token}")
            return None, "Invalid token"

    def has_permission(self, request):
        user, error = self.authenticate_request(request)
        if user:
            request.user = user
            return True
        return False

    def get(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        family_members = FamilyMember.objects.filter(user=user)
        serializer = FamilyMemberSerializer(family_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    def authenticate_request(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None, "No token provided"

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'token':
                return None, "Invalid token format"
        except ValueError:
            return None, "Invalid token format"

        try:
            token_obj = Token.objects.get(key=token)
            print(f"Token found: {token_obj.key}")
            return token_obj.user, None
        except Token.DoesNotExist:
            print(f"Token not found: {token}")
            return None, "Invalid token"

    def has_permission(self, request):
        user, error = self.authenticate_request(request)
        if user:
            request.user = user
            return True
        return False

    def post(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name')
        surname = request.data.get('surname')

        try:
            user_to_delete = User.objects.get(first_name=name, last_name=surname)
            user_to_delete.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
