from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in User model to include a credit balance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} (Credits: {self.credits})"


class UploadedDocument(models.Model):
    """
    Stores documents uploaded by users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} by {self.user.username}"

    class Meta:
        ordering = ['-uploaded_at']


class CreditRequest(models.Model):
    """
    Tracks credit requests made by users.
    """
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.status.title()}"

    class Meta:
        ordering = ['-timestamp']


class AcceptedCreditRequest(models.Model):
    """
    Stores accepted credit requests separately.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Accepted: {self.user.username}"


class RejectedCreditRequest(models.Model):
    """
    Stores rejected credit requests separately.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rejected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rejected: {self.user.username}"
