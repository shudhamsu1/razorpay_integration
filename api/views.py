import json
from django.http import QueryDict
from rest_framework import status
import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order
from .serializers import OrderSerializer

env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


# @api_view(['GET','POST'])
# def start_payment(request):

#     if request.method == 'GET':
#         orders = Order.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)
    

#     elif request.method == 'POST':
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class startPayment(ListCreateAPIView):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

    # def get(self, request, *args, **kwargs):
    #     return Response()

    # def post(self, request, *args, **kwargs):
        
    #     amount = request.data['order_amount']
    #     name = request.data['order_product']
    #     client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
        
    #     # try:
    #     payment = client.order.create({"amount": int(amount) * 100, 
    #                                "currency": "INR", 
    #                                "payment_capture": "1"})
    #     order = Order.objects.create(order_product=name, 
    #                              order_amount=amount, 
    #                              order_payment_id=payment['id'])
    #     serializer = OrderSerializer(order)
        
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     # except:
    #     #  return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

 
        
class paymentnumber(RetrieveUpdateDestroyAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer
        

# @api_view(['GET','POST'])
# def start_payment(request):

#     if request.method == 'POST':
#         name = Order.objects.filter(order_product=request.data['order_product'])
#         amount = Order.objects.filter(order_amount=request.data['order_amount'])
        
#         client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
         
#         payment = client.order.create({"amount": int(amount) * 100, 
#                                    "currency": "INR", 
#                                    "payment_capture": "1"})
#         order = Order.objects.create(order_product=name, 
#                                  order_amount=amount, 
#                                  order_payment_id=payment['id'])
#         serializer = OrderSerializer(order)
        
#         return Response(serializer)