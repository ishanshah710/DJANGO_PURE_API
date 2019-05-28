from django.contrib import admin
from updates.models import Update as UpdateModel
# Register your models here.

class UpdateAdmin(admin.ModelAdmin):
    list_display = [ 'pk','__str__']
    class Meta():
        model = UpdateModel
admin.site.register(UpdateModel , UpdateAdmin)
