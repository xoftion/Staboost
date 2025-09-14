from django.conf import settings
from rest_framework import views, response, status, permissions
from paystackapi.paystack import Paystack
from core.models import Transaction as AppTransaction, User
from .models import Payment
import uuid
import hmac
import hashlib
import json

class InitiatePaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        email = request.user.email

        if not amount:
            return response.Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_float = float(amount)
            # Paystack amount is in kobo
            amount_kobo = int(amount_float * 100)
            reference = f"staboost-{uuid.uuid4()}"

            # Create a Payment record
            Payment.objects.create(
                user=request.user,
                amount=amount_float,
                reference=reference,
                status='pending'
            )

            paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
            paystack_response = paystack.transaction.initialize(
                reference=reference,
                amount=amount_kobo,
                email=email,
                callback_url=request.data.get('callback_url', '')
            )

            if paystack_response['status']:
                return response.Response(paystack_response['data'], status=status.HTTP_200_OK)
            else:
                return response.Response(
                    {"error": paystack_response.get('message', 'Failed to initialize payment.')},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db import transaction

class PaystackWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Verify the event from Paystack
        signature = request.headers.get('x-paystack-signature')
        body = request.body.decode('utf-8')

        hash = hmac.new(settings.PAYSTACK_SECRET_KEY.encode('utf-8'), body.encode('utf-8'), hashlib.sha512).hexdigest()

        if signature != hash:
            return response.Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        event_data = json.loads(body)
        event_type = event_data.get('event')

        if event_type == 'charge.success':
            data = event_data.get('data')
            reference = data.get('reference')

            try:
                payment = Payment.objects.select_for_update().get(reference=reference)
            except Payment.DoesNotExist:
                return response.Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

            if payment.status == 'success':
                # Already processed
                return response.Response(status=status.HTTP_200_OK)

            if payment.status == 'pending':
                payment.status = 'success'
                payment.save()

                user = payment.user
                wallet = user.wallet
                amount = payment.amount

                wallet.balance += amount
                wallet.save()

                AppTransaction.objects.create(
                    wallet=wallet,
                    transaction_type='deposit',
                    amount=amount,
                    description=f"Deposit from Paystack. Reference: {reference}"
                )

                return response.Response(status=status.HTTP_200_OK)

        return response.Response(status=status.HTTP_200_OK)
