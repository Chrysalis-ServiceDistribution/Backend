from django.db import models
from django.contrib.auth.models import User

class StatusChoices(models.TextChoices):
    PENDING = 'P', 'Pending'
    ACCEPTED = 'A', 'Accepted'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'C', 'Completed'
    CANCELLED = 'X', 'Cancelled'

class FieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    RADIO = 'radio', 'Radio'
    CHECKBOX = 'checkbox', 'Checkbox'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'Service created by {self.user.username}, {self.name}, {self.description}'

class Feedback(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserFeedback(models.Model):
    rated_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_received')
    rating_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tasks')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    def __str__(self):
        return f'Task for {self.service.name} by {self.client.username}'

class FormField(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='form_fields')
    type = models.CharField(max_length=10, choices=FieldType.choices)
    prompt = models.CharField(max_length=255)
    index = models.IntegerField()
    choices = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.prompt} ({self.get_type_display()})'

class RequestField(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='request_fields')
    type = models.CharField(max_length=10, choices=FieldType.choices)
    value = models.CharField(max_length=255, blank=True, null=True)
    index = models.IntegerField()
    options = models.JSONField(blank=True, null=True)
    prompt = models.CharField(max_length=255, blank=True, null=True)
    choices = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.get_type_display()} field for Task {self.task.id}'
