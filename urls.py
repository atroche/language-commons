from django.conf.urls.defaults import *
from django.views.static import serve
from uploader.views import upload, success, home, submissions
from uploader.views import generate_static_repo
from settings import MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', upload), 
    (r'^success/$', success),
    (r'^admin/', include(admin.site.urls)),
    (r'^submissions/$', submissions),
    (r'^sr$', generate_static_repo),
    (r'^media/(?P<path>.*)$', serve,
        {'document_root': MEDIA_ROOT}),
)
