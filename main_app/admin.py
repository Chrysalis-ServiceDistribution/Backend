from django.contrib import admin
from .models import Service, Task, FormField, RequestField


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    inlines = [FormFieldInline]


# Register your models here.
admin.site.register(Service)
admin.site.register(Task)
admin.site.register(FormField)
admin.site.register(RequestField)
