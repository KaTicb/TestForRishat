from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'item_bin'

router = routers.DefaultRouter()
router.register(r'item', views.ItemView, basename='item')
router.register(r'order', views.OrderView, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('buy_item/<int:pk>', views.BuySessionItemView.as_view(), name='buy_item'),
    path('buy_order/<int:pk>', views.BuySessionOrderView.as_view(), name='buy_order'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]
