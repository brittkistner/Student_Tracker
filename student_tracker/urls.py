from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from student_tracker import settings

urlpatterns = patterns('',
    # HOME #
    url(r'^home/$', 'checkin.views.home', name='home'),
    # LOGIN AND REGISTER #
    url(r'^$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', 'checkin.views.register', name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    # PASSWORD RESET
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    'django.contrib.auth.views.password_reset_confirm',
    name='password_reset_confirm'),
    # CLASS #
    url(r'^class/$', 'checkin.views.klass', name='class'),
    # url(r'^class/(?P<class_id>\w+)/$', 'checkin.views.klass', name='class'),


    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)