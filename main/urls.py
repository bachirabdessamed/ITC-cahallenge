from django.urls import path
from main.views.authentication import customer_home, forbidden_view, login_view, create_user
from main.views.bank_worker import manage_bank_cards
from main.views.customer_dashboard import user_dashboard
from main.views.customer_views import money_account_view, request_bank_card

urlpatterns = [
    path('login/', login_view, name='login'),
    path('create-user/', create_user, name='create-user'),
    path('customer-home/', customer_home, name='customer_home'),
    path('request_bank_card/', request_bank_card, name='request_bank_card'),
    path('manage_bank_cards/', manage_bank_cards, name='manage_bank_cards'),
    path('forbidden/', forbidden_view, name='forbidden'),
    path('money_account/', money_account_view, name='money_account'),
]
