from rest_framework import serializers
from .models import Transaction, Seller, Sell


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(read_only=True)

    class Meta:
        model = Seller
        fields = '__all__'


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'
