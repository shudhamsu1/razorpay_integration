from django.urls import path

from .views import *

urlpatterns = [
    path('pay/', startPayment.as_view(), name="payment"),
    # path('pay/<int:pk>',paymentnumber.as_view()),
    # path('payment/success/', handle_payment_success, name="payment_success")
]