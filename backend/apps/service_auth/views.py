# service_auth/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer


from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# dodac weryfikacje np email
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            # zapis do bazy danych
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()

            # mock poprawnej odpowiedzi:
            mock_user_data = serializer.validated_data
            return Response({
                "message": "User has been successfully registered (MOCK)",
                "user": {
                    "username": mock_user_data.get("username"),
                    "role": mock_user_data.get("role", "standard"),
                    "data": mock_user_data.get("data", ""),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Podaj login i hasło"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "role": user.role})
        else:
            return Response({"error": "Błędne dane logowania"}, status=status.HTTP_401_UNAUTHORIZED)

        # mock:
        # return Response({
        #     "message": "User logged in successfully (MOCK)",
        #     "token": "mock_token_xyz123abc",
        #     "username": username,
        #     "role": "standard"
        # }, status=status.HTTP_200_OK)