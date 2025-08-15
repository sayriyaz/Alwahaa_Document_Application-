from django.contrib import admin
from .models import Client, Document, Service,Task

admin.site.register(Client)
admin.site.register(Document)
admin.site.register(Service)
admin.site.register(Task)
# Register your models here.
