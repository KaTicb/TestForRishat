from django.http import HttpResponseRedirect, JsonResponse
from django.template.defaultfilters import default
from django.urls import reverse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

import stripe

from .models import *
from .serializer import *

from base.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class ItemView(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'item': serializer.data}, template_name='item_bin/item_detail.html')

    def list(self, request, *args, **kwargs):
        return Response({'items': self.queryset}, template_name='item_bin/item_list.html')


class OrderView(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    queryset = Order.objects.all()

    for order in queryset:
        order.tax = Tax.objects.filter(order=order).first()
        order.tax = order.tax.tax if order.tax else 0.0

        order.discount = Discount.objects.filter(order=order).first()
        order.discount = order.discount.discount if order.discount else 0.0

    def list(self, request, *args, **kwargs):
        return Response({'orders': self.queryset}, template_name='item_bin/order_list.html')


class BuyIntendItemView(APIView):

    def post(self, request, pk):
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST requests are accepted'}, status=405)

        try:

            item = Item.objects.get(id=pk)
            total_price = int(item.price * item.quantity * 100)

            payment_intent = stripe.PaymentIntent.create(
                amount=total_price,
                currency='usd',
                payment_method_types=['card']
            )

            return JsonResponse({
                'clientSecret': payment_intent['client_secret'],
                'paymentIntentId': payment_intent['id']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class BuySessionOrderView(APIView):

    def post(self, request, pk):

        order = Order.objects.get(id=pk)
        discount = Discount.objects.filter(order=order).first()
        tax = Tax.objects.filter(order=order).first()

        total_price = int(sum([item.price * item.quantity for item in order.items.all()]) * 100)

        success_url = request.build_absolute_uri(reverse('item_bin:success'))
        cancel_url = request.build_absolute_uri(reverse('item_bin:cancel'))

        # tax
        if tax:
            tax_rate = stripe.TaxRate.create(
                display_name="Sales Tax",
                description="Sales tax",
                percentage=tax.tax,
                inclusive=False,
            )
        else:
            tax_rate = None

        # discount
        if discount:
            discount_coupon = stripe.Coupon.create(
                percent_off=discount.discount,
                duration='forever',
            )
        else:
            discount_coupon = None

        # payment
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f"{order.user}'s order",
                            },
                            'unit_amount': total_price,
                        },
                        'quantity': 1,
                        'tax_rates': [tax_rate.id,],
                    },
                ],
                discounts=[
                    {
                        'coupon': discount_coupon.id  # ID созданного купона
                    }
                ],
                metadata={
                    'original_amount': str(total_price),
                    'discount_amount': str(discount_coupon.amount_off),
                    'tax_amount': str(tax_rate.percentage)
                },
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(cancel_url)


def success(request):
    return render(request, 'item_bin/success.html')


def cancel(request):
    return render(request, 'item_bin/cancel.html')
