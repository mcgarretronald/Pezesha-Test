from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer, TransferSerializer
from django.db import transaction

class AccountView(APIView):
    # Handle POST requests to create a new account
    def post(self, request):
        """Create a new account."""
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new account if the data is valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle GET requests to retrieve account information
    def get(self, request, id=None):
        """Retrieve account information."""
        try:
            account = Account.objects.get(id=id)  # Fetch account by ID
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

class TransferView(APIView):
    # Handle POST requests to transfer money between accounts
    def post(self, request):
        """Transfer money between accounts."""
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            from_phone = serializer.validated_data['from_phone']
            to_phone = serializer.validated_data['to_phone']
            amount = serializer.validated_data['amount']

            if amount <= 0:
                return Response({"error": "Transfer amount must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():  # Ensure atomicity for the transfer
                    from_account = Account.objects.select_for_update().get(phone=from_phone)
                    to_account = Account.objects.select_for_update().get(phone=to_phone)

                    if from_account.balance < amount:
                        return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

                    # Deduct amount from sender's account and add to receiver's account
                    from_account.balance -= amount
                    to_account.balance += amount

                    from_account.save()
                    to_account.save()

                    return Response({
                        "message": f"You have sent {amount} shillings to {to_account.username}. Your balance is {from_account.balance}."
                    }, status=status.HTTP_200_OK)

            except Account.DoesNotExist:
                return Response({"error": "One or both accounts do not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

