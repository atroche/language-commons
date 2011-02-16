import re
import os
import subprocess
import urllib2
from django.core.management.base import BaseCommand, CommandError
from uploader.models import Item, Identifier
from datetime import datetime
from commons.settings import MEDIA_ROOT, PROJECT_DIR
from uploader.secret import accesskey, secretkey

def log(message):
    log_file = open(os.path.join(PROJECT_DIR, 'error.log'),'a')
    date_str = str(datetime.now())
    full_message = "\n[%s]: %s\n" % (date_str, message)
    log_file.write(full_message)
    log_file.close()

def unique_identifier(identifier):
    url = "http://archive.org/details/" + identifier
    try:
        urllib2.urlopen(url)
        return False
    except urllib2.HTTPError:
        return True

def upload_to_archive(fname, identifier, headers):
    path, last_fname = os.path.split(fname)
    log("Trying to upload '%s' to '%s'." % (fname, identifier))
    remote_fname = "http://s3.us.archive.org/%s/%s" % (identifier, last_fname)
    command = "curl --location %s --upload-file %s %s" % (headers,
        fname, remote_fname)
    log("Running command: " + command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    stdout_value = proc.communicate()[0]
    if stdout_value:
        log("Error: " + stdout_value)
        return False
    else:
        log("Successful upload.")
        return True

def sanitize_for_archive(ident):
    ident = ident.replace(" ", "-")
    ident = re.sub("[^A-Za-z0-9\-_\.]", "", ident)
    print ident
    return ident

def get_first(attr, item, fallback):
    try:
        return eval('item.first("%s").%s' % (attr, attr))
    except:
        return fallback

class Command(BaseCommand):
    help = "Check if any item is waiting to uploaded, then uploads it."

    def handle(self, *args, **options):
        if Item.objects.filter(status="U"):
            return False
        oldest_approved = Item.objects.filter(status="Ap").order_by(
            "time_approved")
        if oldest_approved:
            oldest_approved = oldest_approved[0]
        else:
            return False
        title = get_first("title", oldest_approved, "LanguageCommons-Untitled")
        date = get_first("date", oldest_approved, "Undated")
        language = get_first("contentlanguage", oldest_approved, "eng")
        description = get_first("description", oldest_approved, "")
        ident = "-".join((sanitize_for_archive(title),
            sanitize_for_archive(date)))
        i = 0
        while not unique_identifier(ident):
            ident += str(i)
            i += 1
        if not Identifier.objects.filter(item=oldest_approved):
            Identifier.objects.create(identifier=ident, item=oldest_approved)
        else:
            oldest_approved.first("identifier").identifier = ident
            oldest_approved.first("identifier").save()
        fname = MEDIA_ROOT + oldest_approved.file.file_name.name
        oldest_approved.status = "U" # Uploading
        oldest_approved.save()
        headers = (('x-amz-auto-make-bucket','1'),
                   ('x-archive-meta-mediatype', 'data'),
                   ('x-archive-meta-collection', 'LanguageCommons'),
                   ('x-archive-meta-language', language),
                   ('x-archive-meta-title', title),
                   ('x-archive-meta-description', description.replace("\r\n","")),
                   ('authorization', 'LOW %s:%s' % (accesskey, secretkey)),
                   )
        headers = " ".join(("--header '%s:%s'" % (h, v) for (h, v) in headers))
        if upload_to_archive(fname, ident, headers):
            oldest_approved.status = "Ar" # Archived
        else:
            if oldest_approved.archive_attempts == 3:
                log("Changed %s's status to Error" % oldest_approved)
                oldest_approved.status = "E" # Error
            else:
                oldest_approved.archive_attempts += 1
                oldest_approved.status = "Ap"
        oldest_approved.save()

