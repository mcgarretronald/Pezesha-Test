from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Account

class AccountTests(TestCase):

    def setUp(self):
        # Create sample accounts for testing
        self.account_1 = Account.objects.create(username="JohnDoe", phone="1234567890", balance=1000)
        self.account_2 = Account.objects.create(username="JaneDoe", phone="0987654321", balance=500)

    def test_create_account(self):
        """Test creating a new account with a starting balance"""
        url = reverse('create_account')  # 'create_account' URL name from your urlpatterns
        data = {'username': 'Alice', 'phone': '1122334455', 'balance': 2000}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'Alice')
        self.assertEqual(response.data['phone'], '1122334455')
        self.assertEqual(str(response.data['balance']), '2000.00')  # Adjusted to match the returned format

    def test_get_account(self):
        """Test retrieving account details"""
        url = reverse('get_account', args=[self.account_1.id])  # 'get_account' URL name from your urlpatterns
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'JohnDoe')
        self.assertEqual(response.data['phone'], '1234567890')
        self.assertEqual(str(response.data['balance']), '1000.00')  # Adjusted to match the returned format

    def test_get_non_existent_account(self):
        """Test retrieving account that does not exist"""
        url = reverse('get_account', args=[9999])  # Invalid account ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Account not found')

    def test_transfer_money(self):
        """Test transferring money between accounts"""
        url = reverse('transfer')  # 'transfer' URL name from your urlpatterns
        data = {'from_phone': '1234567890', 'to_phone': '0987654321', 'amount': 100}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check balances after transfer
        self.account_1.refresh_from_db()  # Reload the account to check updated balance
        self.account_2.refresh_from_db()
        
        self.assertEqual(self.account_1.balance, 900)  # 100 deducted from account_1
        self.assertEqual(self.account_2.balance, 600)  # 100 added to account_2

    def test_transfer_money_insufficient_funds(self):
        """Test transfer fails if the source account has insufficient funds"""
        url = reverse('transfer')  # 'transfer' URL name from your urlpatterns
        data = {'from_phone': '1234567890', 'to_phone': '0987654321', 'amount': 2000}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'].strip(), 'Insufficient funds')

    def test_transfer_money_invalid_amount(self):
        """Test transfer fails if the transfer amount is less than or equal to zero"""
        url = reverse('transfer')  # 'transfer' URL name from your urlpatterns
        data = {'from_phone': '1234567890', 'to_phone': '0987654321', 'amount': -100}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'].strip(), 'Transfer amount must be greater than zero')
