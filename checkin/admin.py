from django.contrib import admin
from checkin.models import HelpMe, CheckIn, Class, UserProfile

admin.site.register(UserProfile)
# admin.site.register(Teacher)
# admin.site.register(Student)
admin.site.register(Class)
admin.site.register(CheckIn)
admin.site.register(HelpMe)
