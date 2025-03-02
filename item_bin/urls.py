from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'item_bin'

router = routers.DefaultRouter()
router.register(r'item', views.ItemView, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('buy/<int:pk>', views.BuySessionView.as_view(), name='buy_item'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]
