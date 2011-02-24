from django.contrib import admin
import uploader.models as mods

def inline_factory(model, fk=None):
    """
    Inline classes are needed to edit attributes on the Item's page in the
    admin interface. This function generates one given a model (because
    most of an item's attributes are their own models).
    """
    class Inline(admin.TabularInline): pass
    setattr(Inline, "model", model)
    setattr(Inline, "extra", 0)
    if fk:
        setattr(Inline, "fk_name", fk)
    return Inline


class ItemAdmin(admin.ModelAdmin):
    """
    Necessary for the admin interface to be able to deal with Items nicely.
    If you read the admin docs it'll make sense, it's all standard stuff.
    """
    uploader_models = [mod for mod in mods.models.get_models()
        if "uploader" in str(mod) and "Item" not in str(mod) and "File" not in str(mod)]
    inlines = [inline_factory(mod) for mod in uploader_models]
    inlines += [inline_factory(mods.File)]
    list_display = ('__unicode__', 'status', 'admin_comment')
    list_editable = ('status',)
    list_filter = ('status',)
            
admin.site.register(mods.Item, ItemAdmin)
