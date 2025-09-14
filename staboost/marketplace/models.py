from django.db import models
from django.conf import settings
import uuid

class Service(models.Model):
    PLATFORMS = (
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('x', 'X'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    api_service_id = models.IntegerField(unique=True)
    api_price_per_1000 = models.DecimalField(max_digits=10, decimal_places=4)
    user_price_per_1000 = models.DecimalField(max_digits=10, decimal_places=4, help_text="Price for users per 1000 units.")
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Leave blank to use global markup.")
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Admin notes.")

    def __str__(self):
        return f"{self.name} ({self.platform})"

class Order(models.Model):
    STATUSES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('partial', 'Partial'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
    link = models.URLField(max_length=500)
    username = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    api_order_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
