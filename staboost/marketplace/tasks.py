from celery import shared_task
from .models import Order
from . import cloutflash_api

@shared_task
def update_order_statuses():
    """
    A Celery task to update the status of pending and in-progress orders.
    """
    orders_to_update = Order.objects.filter(status__in=['pending', 'in_progress'])

    for order in orders_to_update:
        try:
            status_data = cloutflash_api.get_order_status(order.api_order_id)
            status = status_data.get('status')

            if status:
                # Map CloutFlash statuses to your app's statuses if they are different
                # For now, assuming they are the same or can be mapped directly
                order.status = status.lower()
                order.save()
        except Exception as e:
            # Handle exceptions, e.g., log the error
            print(f"Error updating status for order {order.id}: {e}")
