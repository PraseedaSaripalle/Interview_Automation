from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    fields = ['topic', 'children', 'level', 'materialized_paths', 'parent_topics']
    list_display = ['topic', 'level', 'parent_topics']
    search_fields = ['topic', 'level']
    autocomplete_fields = ['children'] #https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
    readonly_fields = ('materialized_paths','level', 'parent_topics')

    #raw_id_fields = ("children",) #https://stackoverflow.com/questions/31459078/django-loading-many-to-many-relationship-admin-page-is-so-slow/31459747

    def parent_topics(self, obj):
        r = ", ".join([p.topic for p in obj.parents.all()])
        return r if r else "ROOT"
