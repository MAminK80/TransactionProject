from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TransactionSerializer, BalanceSerializer, SellSerializer
from .models import Transaction, Seller, Sell


class TransactionListView(APIView):
    def get(self, request):
        queryset = Transaction.objects.all()
        serializer = TransactionSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class TransactionAddView(APIView):
    def post(self, request):
        #seller_username = request.POST.get('seller')
        #seller = get_object_or_404(Seller, user__username=seller_username)
        #mutable_data = request.POST.copy()
        #mutable_data['seller'] = seller.id
        #serializer = TransactionSerializer(data=mutable_data)
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Added"})
        return Response(serializer.errors)


class TransactionEachSellerView(APIView):
    def get(self, request, slug):
        seller = Seller.objects.get(slug=slug)

        queryset = Transaction.objects.filter(seller=seller)
        serializer = TransactionSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class TransactionEachView(APIView):
    def get(self, request, pk):
        instance = Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(instance=instance)
        return Response(serializer.data)


class BalanceView(APIView):
    def get(self, request, slug):
        instance = Seller.objects.get(slug=slug)
        serializer = BalanceSerializer(instance=instance)
        return Response(serializer.data)


class SellView(APIView):
    def post(self, request):
        #seller_username = request.POST.get('seller')
        #seller = get_object_or_404(Seller, user__username=seller_username)
        #mutable_data = request.POST.copy()
        #mutable_data['seller'] = seller.id

        #serializer = SellSerializer(data=mutable_data)
        serializer = SellSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Added"})
        return Response(serializer.errors)


class SellListView(APIView):
    def get(self, request):
        queryset = Sell.objects.all()
        serializer = SellSerializer(instance=queryset, many=True)
        return Response(serializer.data)
