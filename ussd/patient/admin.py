from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Patient
# Register your models here.


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "phone_number", "gender", "age")}),
        (
            "Message",
            {
                "fields": (
                    "messageId",
                    "dispatch_time",
                    "status",
                    "time_delivered",
                    "network_code",
                    "failure_reason",
                )
            },
        ),
        (
            "Turn Around",
            {
                "fields": (
                    "interaction_time",
                    "pick_up_date",
                    "TAT"
                )
            }
        )
    )
    list_display = ("username", "phone_number", "dispatch_time", "status", "interaction_time", "pick_up_date", "TAT")
    list_filter = ("dispatch_time", "pick_up_date", "gender", "status")
    search_fields = ("username",)
    # ordering = ("",)