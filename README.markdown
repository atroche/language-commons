CommonsUploader
===============

This is a tool for staging items before they are uploaded to Language Archives, Language Commons, the Universal Corpus or any combination thereof.

It uses cron to run the upload_items management command every minute, which looks for "Approved" items and uploads them to archive.org.

Excact instructions and a shell script for doing this are forthcoming.

Dependencies
============

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

