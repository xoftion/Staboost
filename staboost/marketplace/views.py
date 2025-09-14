from django.conf import settings
from django.conf import settings
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Transaction
from .models import Service, Order
from .serializers import ServiceSerializer, OrderSerializer
from . import cloutflash_api

class FetchServicesView(APIView):
    """
    An admin-only view to fetch services from CloutFlash and populate the database.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            services_data = cloutflash_api.get_services()
            default_markup = settings.DEFAULT_MARKUP_PERCENTAGE

            for service_data in services_data:
                # Basic platform detection, can be improved
                name_lower = service_data['name'].lower()
                platform = 'other'
                if 'instagram' in name_lower:
                    platform = 'instagram'
                elif 'tiktok' in name_lower:
                    platform = 'tiktok'
                elif 'facebook' in name_lower:
                    platform = 'facebook'
                elif 'youtube' in name_lower:
                    platform = 'youtube'
                elif 'twitter' in name_lower or 'x' in name_lower:
                    platform = 'x'

                api_price = float(service_data['rate'])

                service, created = Service.objects.update_or_create(
                    api_service_id=service_data['service'],
                    defaults={
                        'name': service_data['name'],
                        'platform': platform,
                        'api_price_per_1000': api_price,
                        'min_quantity': service_data['min'],
                        'max_quantity': service_data['max'],
                        'description': service_data.get('desc'),
                    }
                )

                markup = service.markup_percentage if service.markup_percentage is not None else default_markup
                user_price = api_price * (1 + markup / 100)
                service.user_price_per_1000 = user_price
                service.save()

            return Response({"message": "Services updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServiceListView(generics.ListAPIView):
    """
    A view to list all active services for users.
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderCreateView(generics.CreateAPIView):
    """
    A view to create a new order.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = serializer.validated_data['service']
        quantity = serializer.validated_data['quantity']

        # Calculate price
        price = (service.user_price_per_1000 / 1000) * quantity

        # Check wallet balance
        wallet = request.user.wallet
        if wallet.balance < price:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct from wallet and create transaction
        wallet.balance -= price
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            transaction_type='order_payment',
            amount=price,
            description=f"Payment for order of {quantity} {service.name}"
        )

        # Place order with CloutFlash
        try:
            api_response = cloutflash_api.place_order(
                service_id=service.api_service_id,
                link=serializer.validated_data['link'],
                quantity=quantity,
                username=serializer.validated_data.get('username')
            )
            api_order_id = api_response.get('order')
        except Exception as e:
            # If API call fails, rollback transaction by raising exception
            raise e

        # Save the order
        order = serializer.save(user=request.user, price=price, api_order_id=api_order_id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
