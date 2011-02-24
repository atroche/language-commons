CommonsUploader
===============

This is a tool for staging items before they are uploaded to the Language Commons. It's written in Python and uses the Django web framework.

Installation
============

Because Django is platform-, database- and webserver-independent, installation really depends on how you want to deploy it. For the [current (as of Feb 2011) Language Commons installation](http://upload.languagecommons.org/), I use Apache (with WSGI) and MySQL for the database. Here's [a handy guide](http://articles.slicehost.com/2009/9/3/ubuntu-hardy-using-mod_wsgi-to-serve-your-application/) to setting up any Django application with a similar stack to what I used.

You need to create a file called secret.py within the 'uploader' app directory. It should contain two variables: 'accesskey' and 'secretkey'. These are not included in the repository for obvious reasons, but they're needed by the part of the application that interfaces with archive.org. Ask an administrator of the Language Commons for account details if you don't already have them.

I use cron to schedule the check for files to be uploaded to the Internet Archive. Here's what mine looks like:
    */1 * * * * /home/atroche/dev/commons/sync_with_archive.sh
This executes a script every single minute. You can change these to suit your priorities -- just consult cron's documentation (don't worry, it's fairly simple.)
All 'sync_with_archive.sh' does here is call './manage.py upload_items', because I've set up all the checking and so on to be a custom Django command. Just call manage.py in the 'commons' directory with that parameter, and it'll take care of the rest.

Other than that, you just need to make sure that your webserver is set up to correctly serve static media from where it's supposed to be served. Just check in settings.py, in commons/media and in the templates to see how I refer to static files (like css, images and js).

If you have any questions, feel free to email me at roche.a [at] gmail [dot] com.

Dependencies
------------

curl
south (Django extension)
django_uni_form (Django extension)

TODO
====

General
-------
More metadata, such as contributor Roles and so on.

Frontend
--------

Backend
-------

