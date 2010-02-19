from django.conf.urls.defaults import *

urlpatterns = patterns('masstext.views',
    url(r'^$', 'masstext', name='masstext'),
)
 
