from django.contrib import admin
from .models import Service, Task, FormField, RequestField

# Register your models here.
admin.site.register(Service)
admin.site.register(Task)
admin.site.register(FormField)
admin.site.register(RequestField)