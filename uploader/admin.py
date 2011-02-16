from django.contrib import admin
import uploader.models as mods

# Whoops, don't need to register every single model...
#for model in mods.models.get_models():
#    if "uploader" in str(model):
#        admin.site.register(model)

#class MetadataInlineAdmin(admin.TabularInline):
#    def __init__(self, model):
#        self.model = model
#        super(MetadataInlineAdmin, self).__init__(model, "uploader")

def inline_factory(model, fk=None):
    class Inline(admin.TabularInline): pass
    setattr(Inline, "model", model)
    setattr(Inline, "extra", 0)
    if fk:
        setattr(Inline, "fk_name", fk)
    return Inline

class DescriptionInline(admin.TabularInline):
    model = mods.Description

class ItemAdmin(admin.ModelAdmin):

    #inlines = [MetadataInlineAdmin(model) for model in mods.models.get_models() if "uploader" in str(model)]
    uploader_models = [mod for mod in mods.models.get_models()
        if "uploader" in str(mod) and "Item" not in str(mod) and "File" not in str(mod)]
    inlines = [inline_factory(mod) for mod in uploader_models]
    inlines += [inline_factory(mods.File)]
    list_display = ('__unicode__', 'status', 'admin_comment')
    list_editable = ('status',)
    list_filter = ('status',)
    #inlines = [DescriptionInline]
    #filter_horizontal = ('descriptions', )
            
admin.site.register(mods.Item, ItemAdmin)
fieldsets = [
    ("Status",      {"fields": ['status', 'admin_comment', 
        'time_approved', 'time_archived']}),
    ("Core",        {"fields": ['titles', 'identifiers', 'dates']} ),
    ("Agents",      {"fields": ['creators', 'publishers']} ),
    ("About",       {"fields": ['subjects', 'descriptions', 'coverages']} ),
    ("Encoding",    {"fields": ['content_languages', 'linguistic_types',
        'DCMI_types', 'subject_languages']} ),
]
