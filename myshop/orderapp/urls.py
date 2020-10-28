import orderapp.views as orderapp
from django.urls import re_path, path

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.OrderList.as_view(), name='orders_list'),
    path('create/', orderapp.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', orderapp.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', orderapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', orderapp.OrderItemsDelete.as_view(), name='order_delete'),
    path('forming/<int:pk>/', orderapp.order_forming_complete, name='order_forming_complete'),
]
