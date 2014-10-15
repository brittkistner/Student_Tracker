from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    name = models.CharField(max_length=25)
    is_student = models.BooleanField(default=True)

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
    class_start = models.DateTimeField()
    class_end = models.DateTimeField()


class CheckIn(models.Model):
    student = models.ForeignKey(UserProfile, related_name="check_ins")
    class_name = models.ForeignKey(Class, related_name="check_ins")
    check_in_time = models.DateTimeField(auto_now_add=True)


class HelpMe(models.Model):
    student = models.ForeignKey(UserProfile, related_name="help_mes")
    created_time = models.DateTimeField(auto_now_add=True)


