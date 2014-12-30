from django.contrib import admin

from logger.models import Car, Entry

class CarAdmin(admin.ModelAdmin):
    pass
admin.site.register(Car, CarAdmin)

class EntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entry, EntryAdmin)


