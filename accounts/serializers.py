from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for account model
    """
    class Meta:
        model = Account
        fields = ['id', 'phone', 'username', 'balance', 'created_at', 'updated_at']


class TransferSerializer(serializers.Serializer):
    """
    Serializer for transferring money between accounts
    """
    from_phone = serializers.CharField(max_length=13)
    to_phone = serializers.CharField(max_length=13)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

