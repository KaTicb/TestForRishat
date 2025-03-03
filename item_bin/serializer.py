from rest_framework.serializers import ModelSerializer
from .models import *


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id']
