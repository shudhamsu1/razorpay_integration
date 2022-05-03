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


# class startPayment(ListCreateAPIView):
#     queryset = Order.objects.none()
#     serializer_class = OrderSerializer

    # def get(self, request, *args, **kwargs):
    #     return Response()

    # def post(self, request, *args, **kwargs):
        ## This data will come from frontend 
    #     amount = request.data['order_amount']
    #     name = request.data['order_product']
    
    ##  This is the client to whom the user is paying
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

 
# This will be able to find objects based on their primary number      
# class paymentnumber(RetrieveUpdateDestroyAPIView):
#         queryset = Order.objects.all()
#         serializer_class = OrderSerializer
        

# @api_view(['GET','POST'])
# def start_payment(request):

#     if request.method == 'POST':
#         name = request.POST.get("order_product")
#         amount = request.POST.get("order_amount")
#         client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
#         payment = client.order.create({"amount": int(amount) * 100, 
#                                    "currency": "INR", 
#                                    "payment_capture": "1"})
#         order = Order.objects.create(order_product=name, 
#                                  order_amount=amount, 
#                                  order_payment_id=payment['id'])
#         serializer = OrderSerializer(order)
        
#         # data = {
#         # "payment": payment,
#         # "order": serializer.data
#         # }
#         return Response(serializer.data)


@api_view(['POST'])
def start_payment(request):
    # The request.data will be passed from the frontend part.
    amount = request.data['amount']
    name = request.data['name']

    #Setting up the razorpay client.This is the client which user is paying. The Public key and secret key is in the .env file
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

   
    # This is creating payment order for razorpay. The amount will come in 'paise' and will be multiplied by 100 and it will be in Rupees
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    
    # This order has just been initialized. The payment wont be made right now.
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)


    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # The data is coming from the frotend
    res = json.loads(request.data["response"])

  # The res will come from the frontend which will be used to confirm and validate the payment
   

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # We can get the order from payment_id
    order = Order.objects.get(order_payment_id=ord_id)

    
    # This data will pass to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    
    # This will check if the transaction is valid or not by passing the data above
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful isPaid= True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)


