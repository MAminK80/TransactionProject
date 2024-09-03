from django.urls import path
from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('transaction_add/', views.TransactionAddView.as_view(), name='transaction_add'),
    path('transaction_each_seller/<slug:slug>', views.TransactionEachSellerView.as_view(),
         name='transaction_each_seller'),
    path('transaction_each/<int:pk>', views.TransactionEachView.as_view(), name='transaction_each'),
    path('balance/<slug:slug>', views.BalanceView.as_view(), name='balance'),
    path('sell/', views.SellView.as_view(), name='sell'),
    path('sell_list/', views.SellListView.as_view(), name='sell_list'),
]
