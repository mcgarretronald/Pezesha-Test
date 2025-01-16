from django.urls import path
from .views import AccountView, TransferView

urlpatterns = [
    path('accounts', AccountView.as_view(), name='create_account'),
    path('accounts/<int:id>', AccountView.as_view(), name='get_account'),
    path('transfers', TransferView.as_view(), name='transfer'),
]
