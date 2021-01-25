from django.contrib import admin

from .models import Handle, Problems


class ProblemsAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'num_sol')


class HandleAdmin(admin.ModelAdmin):
    search_fields = ('name', 'handle')
    list_display = ('name', 'handle', 'batch')


admin.site.register(Handle, ProblemsAdmin)
admin.site.register(Problems, HandleAdmin)
