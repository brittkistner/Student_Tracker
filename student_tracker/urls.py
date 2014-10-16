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
    url(r'^class/(?P<class_id>\d+)$', 'checkin.views.view_class', name='view_class'),
    # url(r'^class2/$', 'checkin.views.klass2', name='class2'),

    url(r'^class/helpMe/$', 'checkin.views.helpme', name='helpme'),
    url(r'^add_help/(?P<student_id>\w+)/$', 'checkin.views.add_help', name='add_help'),
    url(r'^helped/(?P<help_id>\w+)/$', 'checkin.views.helped', name='helped'),
    url(r'^to_teacher/$', 'checkin.views.to_teacher', name='to_teacher'),
    url(r'^to_student/$', 'checkin.views.to_student', name='to_student'),


    url(r'^admin/', include(admin.site.urls)),

    #check in
    url(r'^checkin/$', 'checkin.views.checkin', name='checkin'),
    url(r'^ajax-checkin/$', 'checkin.views.ajax_checkin', name='ajax_checkin'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)