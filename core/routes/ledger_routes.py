from django.urls import path
from core.views.ledger_views import transaction_list, transaction_detail, transaction_reverse

path('gyms/<uuid:gym_id>/transactions/', transaction_list, name = 'transaction-list'),
path('gyms/<uuid:gym_id>/transactions/<uuid:transaction_id>/', transaction_detail, name = 'transaction-detail'),
path('gyms/<uuid:gym_id>/transactions/<uuid:transaction_id>/reverse/', transaction_reverse, name = 'transaction-reverse'),