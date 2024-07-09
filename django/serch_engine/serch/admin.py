from django.contrib import admin
from .models import Engine_name, Detaile_name, search_data

# Register your models here.


class Detaile_nameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ["name"]
    search_fields = ["name"]


class Engine_nameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ["name"]
    search_fields = ["name"]


class Search_dataAdimin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "user",
        "search_user",
        "engine_name",
        "detail_name",
        "keyword",
        "image",
        "created_at",
        "price",
    )


admin.site.register(Detaile_name, Detaile_nameAdmin)
admin.site.register(Engine_name, Engine_nameAdmin)
admin.site.register(search_data, Search_dataAdimin)
