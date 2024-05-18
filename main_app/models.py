from django.db import models
from django.contrib.auth.models import User


class StatusChoices(models.TextChoices):
    PENDING = 'P', 'Pending'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'C', 'Completed'
    CANCELLED = 'X', 'Cancelled'


class FieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    RADIO = 'radio', 'Radio'
    CHECKBOX = 'checkbox', 'Checkbox'


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'Service created by {self.user.username}, {self.name}, {self.description}'


class Task(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tasks')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    req = models.JSONField()
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

    def __str__(self):
        return f'{self.get_type_display()} field for Task {self.task.id}'
