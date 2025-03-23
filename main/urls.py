from django.urls import path
from main.views import transfer_history, transfer_money
from main.views.authentication import customer_home, forbidden_view, login_view, create_user, logout_view
from main.views.bank_worker import manage_bank_cards
from main.views.customer_dashboard import user_dashboard
from main.views.customer_views import money_account_view, request_bank_card, update_profile
from main.views.notification import notifications_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_view, name='login'),
    path('create-user/', create_user, name='create-user'),
    path('customer-home/', customer_home, name='customer_home'),
    path('request_bank_card/', request_bank_card, name='request_bank_card'),
    path('manage_bank_cards/', manage_bank_cards, name='manage_bank_cards'),
    path('forbidden/', forbidden_view, name='forbidden'),
    path('money_account/', money_account_view, name='money_account'),
    path('transfer_money/', transfer_money, name='transfer_money'),
    path('transfer_history/', transfer_history, name='transfer_history'),
    path('notifications/', notifications_view, name='notifications'),
    path('update_profile/', update_profile, name="update_profile"),
    path('logout/', logout_view, name='logout'),
]
