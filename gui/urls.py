from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from gui.views import java_script

dajaxice_autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from gui import views
urlpatterns = patterns('',
		url(r'^$', 'django.contrib.auth.views.login', {'extra_context':{'next':'/app/'}}),
		url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
		url(r'^app/$', 'gui.views.index'),
		url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
		url(r'.*\.js$', java_script),
    # Examples:
    # url(r'^$', 'gui.views.home', name='home'),
    # url(r'^gui/', include('gui.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
