from django.core.mail import send_mail
from django.conf import settings


def send_order_notification(order):
    send_mail(
        subject=f' Order #{order.id} is Received',
        message=f"""

            Hi {order.user.first_name}

            your order #{order.id } has been placed succesfully.

            Total: {order.grand_total}

            thank you for shopping with us.
        
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        fail_silently= False    
    )