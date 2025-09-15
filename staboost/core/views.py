from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Transaction
from .serializers import RegistrationSerializer, UserSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully."
        })

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = self.serializer_class.get_user(request.data)
            now = timezone.now()

            if user.last_rewarded_login is None or now - user.last_rewarded_login > timedelta(days=1):
                reward_amount = settings.DAILY_LOGIN_REWARD_AMOUNT
                wallet = user.wallet
                wallet.balance += reward_amount
                wallet.save()

                Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='login_reward',
                    amount=reward_amount,
                    description='Daily login reward'
                )

                user.last_rewarded_login = now
                user.save()

        return response
