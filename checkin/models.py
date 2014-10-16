from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    # name = models.CharField(max_length=25)
    # we enter first and last names in the registration, the name field is unnecessary
    is_student = models.BooleanField(default=True)
    # I think my database might be screwed up because it doesnt let me make changes to the user
    # in the admin, working around it to avoid dropping the db

    def __unicode__(self):
        return self.username


# class Teacher(UserProfile):
#
#     def __unicode__(self):
#         return u"teacher {}".format(self.first_name)
#
#
# class Student(UserProfile):
#
#     def __unicode__(self):
#         return u"student {}".format(self.first_name)


class Class(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(UserProfile, related_name="classes_teacher")
    student = models.ManyToManyField(UserProfile, related_name="classes_student")
    class_start = models.TimeField()
    class_end = models.TimeField()


class CheckIn(models.Model):
    student = models.ForeignKey(UserProfile, related_name="check_ins")
    class_name = models.ForeignKey(Class, related_name="check_ins")
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{}".format(self.class_name.name)


class HelpMe(models.Model):
    student = models.ForeignKey(UserProfile, related_name="help_mes")
    created_time = models.DateTimeField(auto_now_add=True)
