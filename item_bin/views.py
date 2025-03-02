from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

import stripe

from .models import Item
from .serializer import ItemSerializer

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


class BuySessionView(APIView):

    def post(self, request, pk):

        item = Item.objects.get(id=pk)
        try:
            success_url = request.build_absolute_uri(reverse('item_bin:success'))
            cancel_url = request.build_absolute_uri(reverse('item_bin:cancel'))

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item.name,
                            },
                            'unit_amount': int(item.price * 100),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            print(str(e))
            return HttpResponseRedirect(cancel_url)


def success(request):
    return render(request, 'item_bin/success.html')


def cancel(request):
    return render(request, 'item_bin/cancel.html')
