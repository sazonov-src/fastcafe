from app_order.models import Order


def get_in_process_orders_queryset():
    return Order.objects.filter(created=True, done=False)


def get_order_items_queryset(order_pk: int):
    order = Order.objects.get(pk=order_pk)
    return order.orderitem_set.all()


def mark_order_as_done(instance: Order, data: dict) -> Order:
    if data.get('done', None):
        instance.done = True
        instance.save()
    return instance
