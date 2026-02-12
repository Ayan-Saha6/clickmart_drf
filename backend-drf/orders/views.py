from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart,CartItem
from rest_framework.response import Response
from .models import Order,OrderItem
from .serializers import OrderSerialzer
from rest_framework import status
from .utils import send_order_notification
from rest_framework.generics import ListAPIView





class PlaceOrderView(APIView):
    # the user must be logged in 
    permission_classes=[IsAuthenticated]

    def post(self,request):
        
        # check if the cart is empty
        cart = Cart.objects.get(user=request.user)
        if not cart or cart.items.count() ==0 :
            return Response({'error':'cart is empty'})
        

        # create the order
        order=Order.objects.create(
            user=request.user,
            subtotal = cart.subtotal,
            tax_amount= cart.tax_amount , 
            grand_total= cart.grand_total ,

        )


        # create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order =  order,
                product = item.product,
                quantity = item.quantity ,
                price = item.product.price,
                total_price = item.total_price         # from the cart attribute
            )


        # clear the cart items
        cart.items.all().delete()
        cart.save()


        # sent the notification email
        send_order_notification(order)

        # send the response to frontend
        serializer = OrderSerialzer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class MyOrdersView(ListAPIView):               # here we use the ListAPIView
    permission_classes=[IsAuthenticated]
    serializer_class=OrderSerialzer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)   #this will give the list of addresses of particular user