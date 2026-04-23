from django.contrib import admin
from .models import KS2Form, WorkItem, KS3Form


@admin.register(KS2Form)
class KS2FormAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'customer', 'contractor', 'object_name', 'created_at')
    list_filter = ('customer', 'created_at')
    search_fields = ('document_number', 'customer', 'contractor', 'construction')
    readonly_fields = ('created_at', 'updated_at')


class WorkItemInline(admin.TabularInline):
    model = WorkItem
    extra = 1
    fields = ('position', 'name', 'unit_of_measurement', 'quantity', 'price')


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    list_display = ('ks2_form', 'position', 'name', 'quantity', 'price', 'total')
    list_filter = ('ks2_form', 'unit_of_measurement')
    search_fields = ('name', 'position')
    readonly_fields = ('total',)


@admin.register(KS3Form)
class KS3FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'ks2_form', 'created_at')
    list_filter = ('created_at',)

