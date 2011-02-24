from django.db import models
from django.db.models import CharField, ManyToManyField, DateTimeField,\
    FileField, OneToOneField, BooleanField, OneToOneField, IntegerField,\
    ForeignKey
from datetime import datetime

# From: http://www.language-archives.org/REC/role.html
OLAC_CONTRIBUTOR_ROLES = (
    ('', '---'),
    ('author', 'Author'),
    ('editor', 'Editor'),
)

# From: http://www.language-archives.org/REC/type.html
LINGUISTIC_TYPES = (
    ('', '---'),
    ('lexicon', 'Lexicon'),
    ('primary_text', 'Primary Text'),
    ('language_description', 'Langugage Description'),
)

# From: http://dublincore.org/documents/dcmi-type-vocabulary
DCMI_TYPES = (
    ('', '---'),
    ('collection', 'Collection'),
    ('dataset', 'Dataset'),
    ('event', 'Event'),
    ('image', 'Image'),
    ('interactive_resource', 'Interactive Resource'),
    ('moving_image', 'Moving Image'),
    ('physical_object', 'Phyiscal Object'),
    ('service', 'Service'),
    ('software', 'Software'),
    ('still_image', 'Still Image'),
    ('text', 'Text'),
)

ITEM_STATUSES = (
    ('P', 'Pending'),
    ('R', 'Rejected'),
    ('Ap', 'Approved'),
    ('U', 'Uploading'),
    ('Ar', 'Archived'),
    ('E', "Error"),
)

REJECTION_REASONS = (
    ('I', 'Irrelevant'),
    ('C', 'Corrupt'),
    ('O', 'Other'),
)

class Item(models.Model):
    status = CharField(choices=ITEM_STATUSES, max_length=250, blank=True)
    admin_comment = CharField(blank=True, max_length=250)
    for_universal_corpus = BooleanField()
    provenance = CharField(max_length=100, blank=True)
    rejection_reason = CharField(blank=True, choices=REJECTION_REASONS,
        max_length=1)
    time_added = DateTimeField(auto_now=True)
    time_approved = DateTimeField(null=True, blank=True, editable=False)
    time_archived = DateTimeField(null=True, blank=True, editable=False)
    archive_attempts = IntegerField(default=0, editable=False)

    def first(self, attr):
        """
        Returns the first-specified attribute of the Item.
        """
        attr_list = eval("self.%s_set.all()" % attr.lower())
        if attr_list:
            return attr_list[len(attr_list)-1]
        else:
            return None

    def identifier(self):
        return self.first("identifier")

    def title(self):
        return self.first("title")

    def date(self):
        return self.first("date")

    def __unicode__(self):
        try:
            return self.first("title").title
        except:
            return "No title"

    def save(self, *args, **kwargs):
        """
        If the Item's been archived or approved, record the time at which
        it happened.
        """
        if self.id:
            old_status = Item.objects.get(pk=self.id).status
            if old_status != 'Ar' and self.status == 'Ar':
                self.time_archived = datetime.now()
            elif old_status != 'Ap' and self.status == 'Ap':
                self.time_approved = datetime.now()
        super(Item, self).save(*args, **kwargs)

class File(models.Model):
    file_name = FileField(upload_to="uploads/%Y/%m/%d")
    item = OneToOneField('Item', editable=False)

class Title(models.Model):
    title = CharField(max_length=250)
    item = ForeignKey(Item)
    def __unicode__(self):
        return self.title

class Identifier(models.Model):
    identifier = CharField(max_length=250)
    item = ForeignKey(Item)
    def __unicode__(self):
        return self.identifier

class Date(models.Model):
    date = CharField(max_length=250)
    item = ForeignKey(Item)
    def __unicode__(self):
        return self.date

class Contributor(models.Model):
    contributor = CharField(max_length=250)
    item = ForeignKey(Item)

class Creator(models.Model):
    creator = CharField(max_length=250)
    item = ForeignKey(Item)

class Publisher(models.Model):
    publisher = CharField(max_length=250)
    item = ForeignKey(Item)

class Description(models.Model):
    description = CharField(max_length=250)
    item = ForeignKey(Item)

class LinguisticType(models.Model):
    linguistic_type = CharField(choices=LINGUISTIC_TYPES, max_length=250)
    item = ForeignKey(Item)

class DCMIType(models.Model):
    dcmi_type = CharField(choices=DCMI_TYPES, max_length=250)
    item = ForeignKey(Item)

class ContentLanguage(models.Model):
    language = CharField(max_length=100)
    item = ForeignKey(Item)

class SubjectLanguage(models.Model):
    language = CharField(max_length=100)
    item = ForeignKey(Item)
